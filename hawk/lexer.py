"""
Hawk Programming Language — Lexer (Tokenizer)
"""

from enum import Enum, auto
from typing import List, Optional, Tuple
from hawk.errors import HawkSyntaxError


class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    ID = auto()
    TRUE = auto()
    FALSE = auto()

    # Keywords
    SET = auto()
    PRINT = auto()
    FN = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IMPORT = auto()

    # Logic
    AND = auto()
    OR = auto()
    NOT = auto()

    # Operators
    EQ = auto()          # = (equality check)
    NE = auto()          # !=
    GT = auto()          # >
    LT = auto()          # <
    GTE = auto()         # >=
    LTE = auto()         # <=
    PLUS = auto()        # +
    MINUS = auto()       # -
    STAR = auto()        # *
    SLASH = auto()       # /
    PERCENT = auto()     # % (modulo)
    CARET = auto()       # ^ (exponentiation)
    PRIME = auto()       # ' (transpose)

    # Delimiters
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    COMMA = auto()       # ,
    COLON = auto()       # :
    SEMICOLON = auto()   # ; (inside matrices only)
    NEWLINE = auto()     # \n
    EOF = auto()


class Token:
    def __init__(self, type_: TokenType, value: any, line: int, col: int):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, L{self.line}:C{self.col})"


KEYWORDS = {
    "set": TokenType.SET,
    "print": TokenType.PRINT,
    "fn": TokenType.FN,
    "return": TokenType.RETURN,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "import": TokenType.IMPORT,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}


class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.col = 1
        self.bracket_depth = 0

    def peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx < len(self.code):
            return self.code[idx]
        return ""

    def advance(self) -> str:
        ch = self.peek()
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while self.pos < len(self.code):
            ch = self.peek()
            start_line = self.line
            start_col = self.col

            # 1. Skip whitespace (not newlines)
            if ch in " \t\r":
                self.advance()
                continue

            # 2. Comments: # or //
            if ch == "#" or (ch == "/" and self.peek(1) == "/"):
                while self.pos < len(self.code) and self.peek() != "\n":
                    self.advance()
                continue

            # 3. Newlines
            if ch == "\n":
                self.advance()
                # Emit NEWLINE only when not inside brackets [ ... ]
                if self.bracket_depth == 0:
                    # Avoid consecutive duplicate NEWLINEs
                    if not tokens or tokens[-1].type != TokenType.NEWLINE:
                        tokens.append(Token(TokenType.NEWLINE, "\n", start_line, start_col))
                continue

            # 4. Numbers (including implicit multiplication: 2x -> 2 and x)
            if ch.isdigit() or (ch == "." and self.peek(1).isdigit()):
                num_str = ""
                has_dot = False
                while self.pos < len(self.code):
                    c = self.peek()
                    if c.isdigit():
                        num_str += self.advance()
                    elif c == "." and not has_dot:
                        has_dot = True
                        num_str += self.advance()
                    else:
                        break
                val = float(num_str) if has_dot else float(num_str)
                tokens.append(Token(TokenType.NUMBER, val, start_line, start_col))
                continue

            # 5. String literals "..."
            if ch == '"':
                self.advance() # eat "
                s_chars = []
                while self.pos < len(self.code) and self.peek() != '"':
                    if self.peek() == "\\" and self.pos + 1 < len(self.code):
                        self.advance()
                        escaped = self.advance()
                        if escaped == "n": s_chars.append("\n")
                        elif escaped == "t": s_chars.append("\t")
                        elif escaped == '"': s_chars.append('"')
                        elif escaped == "\\": s_chars.append("\\")
                        else: s_chars.append(escaped)
                    else:
                        s_chars.append(self.advance())
                if self.pos >= len(self.code) or self.peek() != '"':
                    raise HawkSyntaxError("Unterminated string literal (missing closing quote '\"')", line=start_line, col=start_col, end_col=self.col)
                self.advance()
                tokens.append(Token(TokenType.STRING, "".join(s_chars), start_line, start_col))
                continue

            # 6. Identifiers and keywords
            if ch.isalpha() or ch == "_":
                ident = ""
                while self.pos < len(self.code) and (self.peek().isalnum() or self.peek() == "_"):
                    ident += self.advance()
                
                ttype = KEYWORDS.get(ident, TokenType.ID)
                tokens.append(Token(ttype, ident, start_line, start_col))
                continue

            # 7. Two-character operators
            two_ch = self.peek() + self.peek(1)
            if two_ch == "!=":
                self.advance(); self.advance()
                tokens.append(Token(TokenType.NE, "!=", start_line, start_col))
                continue
            elif two_ch == ">=":
                self.advance(); self.advance()
                tokens.append(Token(TokenType.GTE, ">=", start_line, start_col))
                continue
            elif two_ch == "<=":
                self.advance(); self.advance()
                tokens.append(Token(TokenType.LTE, "<=", start_line, start_col))
                continue

            # 8. Single-character operators and brackets
            if ch == "=":
                self.advance()
                tokens.append(Token(TokenType.EQ, "=", start_line, start_col))
            elif ch == ">":
                self.advance()
                tokens.append(Token(TokenType.GT, ">", start_line, start_col))
            elif ch == "<":
                self.advance()
                tokens.append(Token(TokenType.LT, "<", start_line, start_col))
            elif ch == "+":
                self.advance()
                tokens.append(Token(TokenType.PLUS, "+", start_line, start_col))
            elif ch == "-":
                self.advance()
                tokens.append(Token(TokenType.MINUS, "-", start_line, start_col))
            elif ch == "*":
                self.advance()
                tokens.append(Token(TokenType.STAR, "*", start_line, start_col))
            elif ch == "/":
                self.advance()
                tokens.append(Token(TokenType.SLASH, "/", start_line, start_col))
            elif ch == "%":
                self.advance()
                tokens.append(Token(TokenType.PERCENT, "%", start_line, start_col))
            elif ch == "^":
                self.advance()
                tokens.append(Token(TokenType.CARET, "^", start_line, start_col))
            elif ch == "'":
                self.advance()
                tokens.append(Token(TokenType.PRIME, "'", start_line, start_col))
            elif ch == "(":
                self.advance()
                self.bracket_depth += 1
                tokens.append(Token(TokenType.LPAREN, "(", start_line, start_col))
            elif ch == ")":
                self.advance()
                self.bracket_depth = max(0, self.bracket_depth - 1)
                tokens.append(Token(TokenType.RPAREN, ")", start_line, start_col))
            elif ch == "{":
                self.advance()
                tokens.append(Token(TokenType.LBRACE, "{", start_line, start_col))
            elif ch == "}":
                self.advance()
                tokens.append(Token(TokenType.RBRACE, "}", start_line, start_col))
            elif ch == "[":
                self.advance()
                self.bracket_depth += 1
                tokens.append(Token(TokenType.LBRACKET, "[", start_line, start_col))
            elif ch == "]":
                self.advance()
                self.bracket_depth = max(0, self.bracket_depth - 1)
                tokens.append(Token(TokenType.RBRACKET, "]", start_line, start_col))
            elif ch == ",":
                self.advance()
                tokens.append(Token(TokenType.COMMA, ",", start_line, start_col))
            elif ch == ":":
                self.advance()
                tokens.append(Token(TokenType.COLON, ":", start_line, start_col))
            elif ch == ";":
                self.advance()
                tokens.append(Token(TokenType.SEMICOLON, ";", start_line, start_col))
            else:
                bad_char = self.advance()
                raise HawkSyntaxError(f"Unexpected character '{bad_char}'", line=start_line, col=start_col, end_col=start_col + 1)

        # Trailing EOF token
        if not tokens or tokens[-1].type != TokenType.NEWLINE:
            tokens.append(Token(TokenType.NEWLINE, "\n", self.line, self.col))
        tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return tokens
