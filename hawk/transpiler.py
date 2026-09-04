"""
🦅 Hawk Programming Language — C Transpiler & Compiler
Генерирует чистый, понятный Си-код и компилирует его через clang/gcc.
"""

import os
import subprocess
from typing import List, Dict, Tuple, Optional, Any
from hawk.ast_nodes import (
    Stmt, Expr, SetStmt, IndexAssignStmt, PrintStmt, IfStmt, WhileStmt, ForStmt,
    FnDef, ReturnStmt, ExprStmt,
    NumberExpr, StringExpr, VarExpr, MatrixLiteral, MatrixIndexExpr,
    TransposeExpr, BinOpExpr, UnaryOpExpr, CallExpr
)


class CTranspiler:
    def __init__(self):
        self.declared_vars = set(["pi", "e"])
        self.var_types: Dict[str, str] = {
            "pi": "double",
            "e": "double"
        }
        self.fn_signatures: Dict[str, Tuple[str, List[str]]] = {}
        self.matrix_counter = 0
        self.runtime_header_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "runtime", "hawk_matrix.h"
        )

    def transpile(self, stmts: List[Stmt]) -> str:
        # 1. Собираем функции и переменные
        fn_nodes: List[FnDef] = []
        main_stmts: List[Stmt] = []

        for s in stmts:
            if isinstance(s, FnDef):
                fn_nodes.append(s)
                # По умолчанию функции в Hawk возвращают double и принимают double
                self.fn_signatures[s.name] = ("double", ["double"] * len(s.params))
            else:
                main_stmts.append(s)

        out = []
        out.append("/* 🦅 Сгенерировано компилятором Hawk v0.1 */")
        out.append("#include <stdio.h>")
        out.append("#include <stdlib.h>")
        out.append("#include <stdbool.h>")
        out.append("#include <math.h>")
        out.append(f'#include "{self.runtime_header_path}"')
        out.append("")
        out.append("#ifndef M_PI")
        out.append("#define M_PI 3.14159265358979323846")
        out.append("#endif")
        out.append("#define pi M_PI")
        out.append("#define e 2.71828182845904523536")
        out.append("")

        # Прототипы функций
        if fn_nodes:
            out.append("/* --- Прототипы пользовательских функций --- */")
            for f in fn_nodes:
                params_c = ", ".join([f"double {p}" for p in f.params]) if f.params else "void"
                out.append(f"double {f.name}({params_c});")
            out.append("")

        # Реализации функций
        if fn_nodes:
            out.append("/* --- Реализации пользовательских функций --- */")
            for f in fn_nodes:
                out.append(self.transpile_fn(f))
                out.append("")

        # Точка входа main
        out.append("/* --- Точка входа программы --- */")
        out.append("int main(int argc, char **argv) {")
        for s in main_stmts:
            c_code = self.transpile_stmt(s, indent=1)
            if c_code:
                out.append(c_code)
        out.append("    return 0;")
        out.append("}")

        return "\n".join(out)

    def transpile_fn(self, fn: FnDef) -> str:
        params_c = ", ".join([f"double {p}" for p in fn.params]) if fn.params else "void"
        # Локальные переменные функции
        saved_types = dict(self.var_types)
        for p in fn.params:
            self.var_types[p] = "double"

        lines = [f"double {fn.name}({params_c}) {{"]
        for s in fn.body:
            lines.append(self.transpile_stmt(s, indent=1))
        lines.append("    return 0.0;")
        lines.append("}")

        self.var_types = saved_types
        return "\n".join(lines)

    def transpile_stmt(self, stmt: Stmt, indent: int = 1) -> str:
        pad = "    " * indent

        if isinstance(stmt, SetStmt):
            val_code, val_type = self.transpile_expr(stmt.value)
            already_declared = stmt.name in self.declared_vars
            self.var_types[stmt.name] = val_type
            if already_declared:
                return f"{pad}{stmt.name} = {val_code};"
            self.declared_vars.add(stmt.name)
            if val_type == "Matrix*":
                return f"{pad}Matrix *{stmt.name} = {val_code};"
            elif val_type in ("const char*", "char*"):
                return f"{pad}const char *{stmt.name} = {val_code};"
            else:
                return f"{pad}double {stmt.name} = {val_code};"

        if isinstance(stmt, IndexAssignStmt):
            r_code, _ = self.transpile_expr(stmt.row)
            c_code, _ = self.transpile_expr(stmt.column) if stmt.column else ("0", "double")
            val_code, _ = self.transpile_expr(stmt.value)
            return f"{pad}matrix_set({stmt.matrix_name}, (int)({r_code}), (int)({c_code}), {val_code});"

        if isinstance(stmt, PrintStmt):
            lines = []
            for e in stmt.expressions:
                e_code, e_type = self.transpile_expr(e)
                if e_type == "Matrix*":
                    lines.append(f"{pad}printf(\"\\n\"); matrix_print({e_code});")
                elif e_type in ("const char*", "char*"):
                    lines.append(f"{pad}printf(\"%s \", {e_code});")
                elif e_type == "bool":
                    lines.append(f"{pad}printf(\"%s \", ({e_code}) ? \"true\" : \"false\");")
                else:
                    lines.append(f"{pad}printf(\"%g \", (double)({e_code}));")
            lines.append(f'{pad}printf("\\n");')
            return "\n".join(lines)

        if isinstance(stmt, ReturnStmt):
            if stmt.value:
                val_code, _ = self.transpile_expr(stmt.value)
                return f"{pad}return {val_code};"
            return f"{pad}return 0.0;"

        if isinstance(stmt, IfStmt):
            cond_code, _ = self.transpile_expr(stmt.condition)
            lines = [f"{pad}if ({cond_code}) {{"]
            for s in stmt.then_body:
                lines.append(self.transpile_stmt(s, indent + 1))
            if stmt.else_body:
                lines.append(f"{pad}}} else {{")
                for s in stmt.else_body:
                    lines.append(self.transpile_stmt(s, indent + 1))
            lines.append(f"{pad}}}")
            return "\n".join(lines)

        if isinstance(stmt, WhileStmt):
            cond_code, _ = self.transpile_expr(stmt.condition)
            lines = [f"{pad}while ({cond_code}) {{"]
            for s in stmt.body:
                lines.append(self.transpile_stmt(s, indent + 1))
            lines.append(f"{pad}}}")
            return "\n".join(lines)

        if isinstance(stmt, ForStmt):
            init_c = self.transpile_stmt(stmt.init, 0).strip().rstrip(";") if stmt.init else ""
            cond_c, _ = self.transpile_expr(stmt.condition) if stmt.condition else ("1", "bool")
            step_c = self.transpile_stmt(stmt.step, 0).strip().rstrip(";") if stmt.step else ""
            lines = [f"{pad}for ({init_c}; {cond_c}; {step_c}) {{"]
            for s in stmt.body:
                lines.append(self.transpile_stmt(s, indent + 1))
            lines.append(f"{pad}}}")
            return "\n".join(lines)

        if isinstance(stmt, ExprStmt):
            code, _ = self.transpile_expr(stmt.expr)
            return f"{pad}{code};"

        return ""

    def transpile_expr(self, expr: Expr) -> Tuple[str, str]:
        """Возвращает кортеж: (C-код выражения, тип в C: 'double' | 'Matrix*' | 'const char*' | 'bool')"""
        if isinstance(expr, NumberExpr):
            v = expr.value
            return (f"{v}", "double")

        if isinstance(expr, StringExpr):
            s = expr.value.replace('"', '\\"')
            return (f'"{s}"', "const char*")

        if isinstance(expr, VarExpr):
            t = self.var_types.get(expr.name, "double")
            return (expr.name, t)

        if isinstance(expr, MatrixLiteral):
            rows = len(expr.rows)
            cols = len(expr.rows[0]) if rows > 0 else 0
            self.matrix_counter += 1
            arr_name = f"_mat_data_{self.matrix_counter}"
            flat_vals = []
            for r in expr.rows:
                for elem in r:
                    c_elem, _ = self.transpile_expr(elem)
                    flat_vals.append(c_elem)
            vals_str = ", ".join(flat_vals)
            # В C вернем вызов matrix_from_array
            return (f"matrix_from_array({rows}, {cols}, (double[]){{{vals_str}}})", "Matrix*")

        if isinstance(expr, MatrixIndexExpr):
            m_code, _ = self.transpile_expr(expr.matrix)
            r_code, _ = self.transpile_expr(expr.row)
            c_code, _ = self.transpile_expr(expr.column) if expr.column else ("0", "double")
            return (f"matrix_get({m_code}, (int)({r_code}), (int)({c_code}))", "double")

        if isinstance(expr, TransposeExpr):
            m_code, _ = self.transpile_expr(expr.matrix)
            return (f"matrix_transpose({m_code})", "Matrix*")

        if isinstance(expr, UnaryOpExpr):
            op_code, op_type = self.transpile_expr(expr.operand)
            if expr.op == "-":
                if op_type == "Matrix*":
                    return (f"matrix_scale({op_code}, -1.0)", "Matrix*")
                return (f"(-({op_code}))", "double")
            if expr.op == "not":
                return (f"(!({op_code}))", "bool")

        if isinstance(expr, BinOpExpr):
            l_code, l_type = self.transpile_expr(expr.left)
            r_code, r_type = self.transpile_expr(expr.right)
            op = expr.op

            # Матричные операции
            if l_type == "Matrix*" or r_type == "Matrix*":
                if op == "*":
                    if l_type == "Matrix*" and r_type == "Matrix*":
                        return (f"matrix_mult({l_code}, {r_code})", "Matrix*")
                    if l_type == "Matrix*":
                        return (f"matrix_scale({l_code}, {r_code})", "Matrix*")
                    return (f"matrix_scale({r_code}, {l_code})", "Matrix*")
                if op == "+":
                    return (f"matrix_add({l_code}, {r_code})", "Matrix*")
                if op == "-":
                    return (f"matrix_sub({l_code}, {r_code})", "Matrix*")

            # Арифметика скаляров
            if op == "+": return (f"({l_code} + {r_code})", "double")
            if op == "-": return (f"({l_code} - {r_code})", "double")
            if op == "*": return (f"({l_code} * {r_code})", "double")
            if op == "/": return (f"({l_code} / {r_code})", "double")
            if op == "^": return (f"pow({l_code}, {r_code})", "double")

            # Сравнения: = в Hawk компилируется в == в C!
            if op == "=": return (f"({l_code} == {r_code})", "bool")
            if op == "!=": return (f"({l_code} != {r_code})", "bool")
            if op == ">": return (f"({l_code} > {r_code})", "bool")
            if op == "<": return (f"({l_code} < {r_code})", "bool")
            if op == ">=": return (f"({l_code} >= {r_code})", "bool")
            if op == "<=": return (f"({l_code} <= {r_code})", "bool")
            if op == "and": return (f"({l_code} && {r_code})", "bool")
            if op == "or": return (f"({l_code} || {r_code})", "bool")

        if isinstance(expr, CallExpr):
            # Встроенные функции
            if expr.callee == "input":
                arg_code = self.transpile_expr(expr.args[0])[0] if expr.args else '""'
                return (f"hawk_input_str({arg_code})", "char*")
            if expr.callee == "input_num":
                arg_code = self.transpile_expr(expr.args[0])[0] if expr.args else '""'
                return (f"hawk_input_num({arg_code})", "double")
            if expr.callee == "det":
                m_code, _ = self.transpile_expr(expr.args[0])
                return (f"matrix_det({m_code})", "double")
            if expr.callee in ("sin", "cos", "tan", "sqrt", "abs", "exp", "log", "round", "floor", "ceil"):
                c_fn = "fabs" if expr.callee == "abs" else expr.callee
                arg_code, _ = self.transpile_expr(expr.args[0])
                return (f"{c_fn}({arg_code})", "double")

            # Пользовательские функции
            args_c = [self.transpile_expr(a)[0] for a in expr.args]
            return (f"{expr.callee}({', '.join(args_c)})", "double")

        return ("0.0", "double")

    def build_native(self, stmts: List[Stmt], output_binary_path: str) -> str:
        c_code = self.transpile(stmts)
        c_temp_file = output_binary_path + ".c"
        with open(c_temp_file, "w", encoding="utf-8") as f:
            f.write(c_code)

        # Компиляция через clang (на macOS всегда доступен clang)
        cmd = [
            "clang",
            "-O3",
            f"-I{os.path.dirname(self.runtime_header_path)}",
            c_temp_file,
            "-o", output_binary_path,
            "-lm"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Ошибка компиляции C-кода (clang):\n{res.stderr}")

        return output_binary_path
