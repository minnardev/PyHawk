"""
🦅 Hawk Programming Language — AST Nodes
"""

from dataclasses import dataclass
from typing import List, Optional, Any


class ASTNode:
    def __init__(self, line: int = 1, col: int = 1):
        self.line = line
        self.col = col


# --- Expressions ---

class Expr(ASTNode):
    pass


@dataclass
class NumberExpr(Expr):
    value: float
    line: int = 1
    col: int = 1


@dataclass
class StringExpr(Expr):
    value: str
    line: int = 1
    col: int = 1


@dataclass
class BoolExpr(Expr):
    value: bool
    line: int = 1
    col: int = 1


@dataclass
class VarExpr(Expr):
    name: str
    line: int = 1
    col: int = 1


@dataclass
class MatrixLiteral(Expr):
    # rows: список строк, каждая строка — список выражений
    # [[1, 2], [3, 4]]
    rows: List[List[Expr]]
    line: int = 1
    col: int = 1


@dataclass
class MatrixIndexExpr(Expr):
    matrix: Expr
    row: Expr
    column: Optional[Expr] = None  # для m[r, c] или v[r]
    line: int = 1
    src_col: int = 1


@dataclass
class TransposeExpr(Expr):
    # m'
    matrix: Expr
    line: int = 1
    col: int = 1


@dataclass
class BinOpExpr(Expr):
    op: str
    left: Expr
    right: Expr
    line: int = 1
    col: int = 1


@dataclass
class UnaryOpExpr(Expr):
    op: str
    operand: Expr
    line: int = 1
    col: int = 1


@dataclass
class CallExpr(Expr):
    callee: str
    args: List[Expr]
    line: int = 1
    col: int = 1


# --- Statements ---

class Stmt(ASTNode):
    pass


@dataclass
class SetStmt(Stmt):
    name: str
    type_annotation: Optional[str]
    value: Expr
    line: int = 1
    col: int = 1


@dataclass
class IndexAssignStmt(Stmt):
    # m[r, c] = expr
    matrix_name: str
    row: Expr
    column: Optional[Expr]
    value: Expr
    line: int = 1
    src_col: int = 1


@dataclass
class PrintStmt(Stmt):
    expressions: List[Expr]
    line: int = 1
    col: int = 1


@dataclass
class IfStmt(Stmt):
    condition: Expr
    then_body: List[Stmt]
    else_body: List[Stmt]
    line: int = 1
    col: int = 1


@dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: List[Stmt]
    line: int = 1
    col: int = 1


@dataclass
class ForStmt(Stmt):
    init: Optional[Stmt]
    condition: Optional[Expr]
    step: Optional[Stmt]
    body: List[Stmt]
    line: int = 1
    col: int = 1


@dataclass
class FnDef(Stmt):
    name: str
    params: List[str]
    body: List[Stmt]
    line: int = 1
    col: int = 1


@dataclass
class ReturnStmt(Stmt):
    value: Optional[Expr]
    line: int = 1
    col: int = 1


@dataclass
class ExprStmt(Stmt):
    expr: Expr
    line: int = 1
    col: int = 1
