"""
🦅 Hawk Programming Language — Parser (Синтаксический анализатор)
"""

from typing import List, Optional
from hawk.lexer import Token, TokenType
from hawk.ast_nodes import (
    Stmt, Expr, SetStmt, IndexAssignStmt, PrintStmt, IfStmt, WhileStmt, ForStmt,
    FnDef, ReturnStmt, ExprStmt,
    NumberExpr, StringExpr, VarExpr, MatrixLiteral, MatrixIndexExpr,
    TransposeExpr, BinOpExpr, UnaryOpExpr, CallExpr
)


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def advance(self) -> Token:
        tok = self.peek()
        if tok.type != TokenType.EOF:
            self.pos += 1
        return tok

    def match(self, *types: TokenType) -> bool:
        if self.peek().type in types:
            self.advance()
            return True
        return False

    def expect(self, type_: TokenType, error_msg: Optional[str] = None) -> Token:
        tok = self.peek()
        if tok.type == type_:
            return self.advance()
        msg = error_msg or f"Hawk SyntaxError: Ожидался токен {type_.name}, а получен {tok.type.name} ('{tok.value}') на строке {tok.line}, столбец {tok.col}"
        raise SyntaxError(msg)

    def skip_newlines(self):
        while self.peek().type in (TokenType.NEWLINE, TokenType.SEMICOLON):
            self.advance()

    # --- Главная точка входа ---

    def parse(self) -> List[Stmt]:
        stmts: List[Stmt] = []
        self.skip_newlines()

        while self.peek().type != TokenType.EOF:
            stmt = self.parse_stmt()
            if stmt:
                stmts.append(stmt)
            self.skip_newlines()

        return stmts

    # --- Инструкции (Statements) ---

    def parse_stmt(self) -> Stmt:
        tok = self.peek()

        # 1. set name [: type] = expr
        if tok.type == TokenType.SET:
            return self.parse_set_stmt()

        # 2. print expr, expr, ...
        if tok.type == TokenType.PRINT:
            return self.parse_print_stmt()

        # 3. fn name(p1, p2) { ... }
        if tok.type == TokenType.FN:
            return self.parse_fn_def()

        # 4. return [expr]
        if tok.type == TokenType.RETURN:
            return self.parse_return_stmt()

        # 5. if (cond) { ... } else { ... }
        if tok.type == TokenType.IF:
            return self.parse_if_stmt()

        # 6. while (cond) { ... }
        if tok.type == TokenType.WHILE:
            return self.parse_while_stmt()

        # 7. for (init; cond; step) { ... }
        if tok.type == TokenType.FOR:
            return self.parse_for_stmt()

        # 8. Проверка на ошибочное голое присваивание без set: x = 5
        if tok.type == TokenType.ID:
            next_tok = self.peek(1)
            # m[r, c] = val
            if next_tok.type == TokenType.LBRACKET:
                # Попробуем разобрать m[r, c] = expr
                return self.parse_index_assign()
            elif next_tok.type == TokenType.EQ:
                raise SyntaxError(
                    f"Hawk Error (строка {tok.line}): Присваивание переменной требует ключевое слово 'set'.\n"
                    f"  Вместо '{tok.value} = ...' напишите: 'set {tok.value} = ...'\n"
                    f"  (В Hawk знак '=' внутри выражений означает только проверку равенства)."
                )

        # Выражение как инструкция (например вызов функции)
        expr = self.parse_expr()
        return ExprStmt(expr, line=tok.line, col=tok.col)

    def parse_set_stmt(self) -> SetStmt:
        start_tok = self.expect(TokenType.SET)
        name_tok = self.expect(TokenType.ID, "Ожидалось имя переменной после 'set'")
        type_annot = None

        if self.match(TokenType.COLON):
            type_tok = self.expect(TokenType.ID, "Ожидался тип после ':'")
            type_annot = type_tok.value

        self.expect(TokenType.EQ, "Ожидался знак '=' после имени переменной в 'set'")
        val_expr = self.parse_expr()
        return SetStmt(name=name_tok.value, type_annotation=type_annot, value=val_expr,
                       line=start_tok.line, col=start_tok.col)

    def parse_index_assign(self) -> Stmt:
        name_tok = self.expect(TokenType.ID)
        self.expect(TokenType.LBRACKET)
        r_expr = self.parse_expr()
        c_expr = None
        if self.match(TokenType.COMMA):
            c_expr = self.parse_expr()
        self.expect(TokenType.RBRACKET)

        if self.match(TokenType.EQ):
            val_expr = self.parse_expr()
            return IndexAssignStmt(matrix_name=name_tok.value, row=r_expr, column=c_expr, value=val_expr,
                                   line=name_tok.line, src_col=name_tok.col)
        else:
            # Это просто выражение m[r, c]
            base_node = VarExpr(name_tok.value, name_tok.line, name_tok.col)
            idx_expr = MatrixIndexExpr(base_node, r_expr, column=c_expr, line=name_tok.line, src_col=name_tok.col)
            return ExprStmt(self.parse_postfix_continue(idx_expr))

    def parse_print_stmt(self) -> PrintStmt:
        start_tok = self.expect(TokenType.PRINT)
        exprs: List[Expr] = []

        if self.peek().type not in (TokenType.NEWLINE, TokenType.EOF, TokenType.RBRACE):
            exprs.append(self.parse_expr())
            while self.match(TokenType.COMMA):
                exprs.append(self.parse_expr())

        return PrintStmt(expressions=exprs, line=start_tok.line, col=start_tok.col)

    def parse_fn_def(self) -> FnDef:
        start_tok = self.expect(TokenType.FN)
        name_tok = self.expect(TokenType.ID, "Ожидалось имя функции после 'fn'")
        self.expect(TokenType.LPAREN, "Ожидалась '(' после имени функции")
        params: List[str] = []

        if self.peek().type != TokenType.RPAREN:
            p_tok = self.expect(TokenType.ID, "Ожидалось имя параметра")
            params.append(p_tok.value)
            while self.match(TokenType.COMMA):
                p_tok = self.expect(TokenType.ID, "Ожидалось имя параметра")
                params.append(p_tok.value)

        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE, "Ожидалась '{' перед телом функции")
        body = self.parse_block()
        return FnDef(name=name_tok.value, params=params, body=body, line=start_tok.line, col=start_tok.col)

    def parse_return_stmt(self) -> ReturnStmt:
        start_tok = self.expect(TokenType.RETURN)
        val: Optional[Expr] = None
        if self.peek().type not in (TokenType.NEWLINE, TokenType.EOF, TokenType.RBRACE):
            val = self.parse_expr()
        return ReturnStmt(value=val, line=start_tok.line, col=start_tok.col)

    def parse_if_stmt(self) -> IfStmt:
        start_tok = self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN, "Ожидалась '(' после 'if'")
        cond = self.parse_expr()
        self.expect(TokenType.RPAREN, "Ожидалась ')' после условия 'if'")
        self.expect(TokenType.LBRACE, "Ожидалась '{' перед телом 'if'")
        then_body = self.parse_block()
        else_body: List[Stmt] = []

        self.skip_newlines()
        if self.match(TokenType.ELSE):
            self.expect(TokenType.LBRACE, "Ожидалась '{' перед телом 'else'")
            else_body = self.parse_block()

        return IfStmt(condition=cond, then_body=then_body, else_body=else_body,
                      line=start_tok.line, col=start_tok.col)

    def parse_while_stmt(self) -> WhileStmt:
        start_tok = self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN, "Ожидалась '(' после 'while'")
        cond = self.parse_expr()
        self.expect(TokenType.RPAREN, "Ожидалась ')' после условия 'while'")
        self.expect(TokenType.LBRACE, "Ожидалась '{' перед телом 'while'")
        body = self.parse_block()
        return WhileStmt(condition=cond, body=body, line=start_tok.line, col=start_tok.col)

    def parse_for_stmt(self) -> ForStmt:
        start_tok = self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)
        init_stmt = self.parse_stmt() if self.peek().type != TokenType.SEMICOLON else None
        self.expect(TokenType.SEMICOLON)
        cond_expr = self.parse_expr() if self.peek().type != TokenType.SEMICOLON else None
        self.expect(TokenType.SEMICOLON)
        step_stmt = self.parse_stmt() if self.peek().type != TokenType.RPAREN else None
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        return ForStmt(init=init_stmt, condition=cond_expr, step=step_stmt, body=body,
                       line=start_tok.line, col=start_tok.col)

    def parse_block(self) -> List[Stmt]:
        stmts: List[Stmt] = []
        self.skip_newlines()
        while self.peek().type not in (TokenType.RBRACE, TokenType.EOF):
            stmt = self.parse_stmt()
            if stmt:
                stmts.append(stmt)
            self.skip_newlines()
        self.expect(TokenType.RBRACE, "Ожидалась '}' в конце блока")
        return stmts

    # --- Выражения (Expressions) ---

    def parse_expr(self) -> Expr:
        return self.parse_or()

    def parse_or(self) -> Expr:
        left = self.parse_and()
        while self.match(TokenType.OR):
            right = self.parse_and()
            left = BinOpExpr(op="or", left=left, right=right, line=left.line, col=left.col)
        return left

    def parse_and(self) -> Expr:
        left = self.parse_comparison()
        while self.match(TokenType.AND):
            right = self.parse_comparison()
            left = BinOpExpr(op="and", left=left, right=right, line=left.line, col=left.col)
        return left

    def parse_comparison(self) -> Expr:
        left = self.parse_additive()
        comp_ops = (TokenType.EQ, TokenType.NE, TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE)

        # Поддержка цепочек сравнений: 1 < r < 10 -> (1 < r) and (r < 10)
        comparisons = []
        while self.peek().type in comp_ops:
            op_tok = self.advance()
            op_str = op_tok.value
            right = self.parse_additive()
            comparisons.append((op_str, right))

        if not comparisons:
            return left

        if len(comparisons) == 1:
            op_str, right = comparisons[0]
            return BinOpExpr(op=op_str, left=left, right=right, line=left.line, col=left.col)

        # Цепочка: left op1 right1 and right1 op2 right2
        # Разворачиваем в and
        curr_left = left
        combined = None
        for op_str, curr_right in comparisons:
            comp_node = BinOpExpr(op=op_str, left=curr_left, right=curr_right, line=curr_left.line, col=curr_left.col)
            if combined is None:
                combined = comp_node
            else:
                combined = BinOpExpr(op="and", left=combined, right=comp_node, line=combined.line, col=combined.col)
            curr_left = curr_right
        return combined

    def parse_additive(self) -> Expr:
        left = self.parse_multiplicative()
        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op_tok = self.advance()
            right = self.parse_multiplicative()
            left = BinOpExpr(op=op_tok.value, left=left, right=right, line=left.line, col=left.col)
        return left

    def parse_multiplicative(self) -> Expr:
        left = self.parse_power()

        while True:
            # Явное умножение / деление
            if self.peek().type in (TokenType.STAR, TokenType.SLASH):
                op_tok = self.advance()
                right = self.parse_power()
                left = BinOpExpr(op=op_tok.value, left=left, right=right, line=left.line, col=left.col)
                continue

            # Неявное умножение только для чисел и переменных (не для строк!)
            if isinstance(left, StringExpr):
                break

            next_t = self.peek().type
            if next_t in (TokenType.NUMBER, TokenType.ID, TokenType.LPAREN):
                if self.peek().value not in ("and", "or", "not"):
                    right = self.parse_power()
                    if isinstance(right, StringExpr):
                        break
                    left = BinOpExpr(op="*", left=left, right=right, line=left.line, col=left.col)
                    continue
            break

        return left

    def parse_power(self) -> Expr:
        left = self.parse_unary()
        if self.match(TokenType.CARET):
            right = self.parse_power() # правоассоциативно: 2^3^4 = 2^(3^4)
            return BinOpExpr(op="^", left=left, right=right, line=left.line, col=left.col)
        return left

    def parse_unary(self) -> Expr:
        if self.match(TokenType.MINUS):
            operand = self.parse_unary()
            return UnaryOpExpr(op="-", operand=operand, line=operand.line, col=operand.col)
        if self.match(TokenType.NOT):
            operand = self.parse_unary()
            return UnaryOpExpr(op="not", operand=operand, line=operand.line, col=operand.col)
        return self.parse_postfix()

    def parse_postfix(self) -> Expr:
        node = self.parse_primary()
        return self.parse_postfix_continue(node)

    def parse_postfix_continue(self, node: Expr) -> Expr:
        while True:
            # Транспонирование: m'
            if self.match(TokenType.PRIME):
                node = TransposeExpr(matrix=node, line=node.line, col=node.col)
                continue

            # Индексация: m[r, c] или v[r]
            if self.match(TokenType.LBRACKET):
                r_expr = self.parse_expr()
                c_expr = None
                if self.match(TokenType.COMMA):
                    c_expr = self.parse_expr()
                self.expect(TokenType.RBRACKET, "Ожидалась ']' после индекса матрицы")
                node = MatrixIndexExpr(matrix=node, row=r_expr, column=c_expr, line=node.line, src_col=getattr(node, "src_col", getattr(node, "col", 1)))
                continue

            # Вызов функции: f(a, b)
            if self.match(TokenType.LPAREN):
                args = []
                if self.peek().type != TokenType.RPAREN:
                    args.append(self.parse_expr())
                    while self.match(TokenType.COMMA):
                        args.append(self.parse_expr())
                self.expect(TokenType.RPAREN, "Ожидалась ')' после аргументов функции")
                if isinstance(node, VarExpr):
                    node = CallExpr(callee=node.name, args=args, line=node.line, col=node.col)
                else:
                    raise SyntaxError(f"Hawk Error: Вызов допустим только для функций (строка {node.line})")
                continue

            break

        return node

    def parse_primary(self) -> Expr:
        tok = self.peek()

        # Число
        if self.match(TokenType.NUMBER):
            return NumberExpr(value=tok.value, line=tok.line, col=tok.col)

        # Строка
        if self.match(TokenType.STRING):
            return StringExpr(value=tok.value, line=tok.line, col=tok.col)

        # Идентификатор / Переменная
        if self.match(TokenType.ID):
            return VarExpr(name=tok.value, line=tok.line, col=tok.col)

        # Выражение в скобках (expr)
        if self.match(TokenType.LPAREN):
            expr = self.parse_expr()
            self.expect(TokenType.RPAREN, "Ожидалась ')'")
            return expr

        # Литерал матрицы [1, 2 ; 3, 4]
        if self.match(TokenType.LBRACKET):
            return self.parse_matrix_literal(tok)

        raise SyntaxError(f"Hawk SyntaxError: Неожиданный токен {tok.type.name} ('{tok.value}') на строке {tok.line}, столбец {tok.col}")

    def parse_matrix_literal(self, start_tok: Token) -> MatrixLiteral:
        rows: List[List[Expr]] = []
        curr_row: List[Expr] = []

        self.skip_newlines()
        if self.match(TokenType.RBRACKET):
            return MatrixLiteral(rows=[], line=start_tok.line, col=start_tok.col)

        while self.peek().type not in (TokenType.RBRACKET, TokenType.EOF):
            # Парсим элемент строки
            elem = self.parse_expr()
            curr_row.append(elem)

            # Разделители внутри строки матрицы: запятая или пробел
            if self.match(TokenType.COMMA):
                pass

            # Разделитель строк матрицы: точка с запятой ';' или перевод строки
            if self.match(TokenType.SEMICOLON) or self.peek().type == TokenType.NEWLINE:
                if self.peek().type == TokenType.NEWLINE:
                    self.advance()
                rows.append(curr_row)
                curr_row = []
                self.skip_newlines()

        if curr_row:
            rows.append(curr_row)

        self.expect(TokenType.RBRACKET, "Ожидалась ']' в конце матрицы")
        return MatrixLiteral(rows=rows, line=start_tok.line, col=start_tok.col)
