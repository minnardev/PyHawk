"""
Hawk Programming Language — Interpreter (Python Runtime)
"""

import os
import sys
import math
import subprocess
from typing import Any, Dict, List, Optional, Set
from hawk.ast_nodes import (
    Stmt, Expr, SetStmt, IndexAssignStmt, PrintStmt, IfStmt, WhileStmt, ForStmt,
    FnDef, ReturnStmt, ExprStmt, ImportStmt,
    NumberExpr, StringExpr, BoolExpr, VarExpr, MatrixLiteral, MatrixIndexExpr,
    TransposeExpr, BinOpExpr, UnaryOpExpr, CallExpr
)


class ReturnSignal(Exception):
    def __init__(self, value: Any):
        self.value = value


class HawkMatrix:
    def __init__(self, rows: int, cols: int, data: Optional[List[float]] = None):
        self.rows = rows
        self.cols = cols
        if data is not None:
            self.data = list(data)
        else:
            self.data = [0.0] * (rows * cols)

    def get(self, r: int, c: int) -> float:
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.data[r * self.cols + c]
        raise IndexError(f"Hawk MatrixError: Index [{r}, {c}] out of bounds for {self.rows}x{self.cols}")

    def set(self, r: int, c: int, val: float):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.data[r * self.cols + c] = float(val)
        else:
            raise IndexError(f"Hawk MatrixError: Index [{r}, {c}] out of bounds for {self.rows}x{self.cols}")

    def transpose(self) -> 'HawkMatrix':
        res = HawkMatrix(self.cols, self.rows)
        for r in range(self.rows):
            for c in range(self.cols):
                res.set(c, r, self.get(r, c))
        return res

    def mult(self, other: Any) -> Any:
        if isinstance(other, (int, float)):
            # Scalar multiplication
            return HawkMatrix(self.rows, self.cols, [x * other for x in self.data])
        if isinstance(other, HawkMatrix):
            if self.cols != other.rows:
                raise ValueError(f"Hawk MatrixError: Cannot multiply matrices of dimensions {self.rows}x{self.cols} and {other.rows}x{other.cols}")
            res = HawkMatrix(self.rows, other.cols)
            for r in range(self.rows):
                for c in range(other.cols):
                    s = sum(self.get(r, k) * other.get(k, c) for k in range(self.cols))
                    res.set(r, c, s)
            return res
        raise TypeError(f"Hawk TypeError: Unsupported matrix multiplication by {type(other)}")

    def add(self, other: 'HawkMatrix') -> 'HawkMatrix':
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Hawk MatrixError: Matrix dimensions do not match for addition")
        return HawkMatrix(self.rows, self.cols, [a + b for a, b in zip(self.data, other.data)])

    def sub(self, other: 'HawkMatrix') -> 'HawkMatrix':
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Hawk MatrixError: Matrix dimensions do not match for subtraction")
        return HawkMatrix(self.rows, self.cols, [a - b for a, b in zip(self.data, other.data)])

    def det(self) -> float:
        if self.rows != self.cols:
            raise ValueError("Hawk MatrixError: Determinant is only defined for square matrices")
        n = self.rows
        if n == 1:
            return self.data[0]
        if n == 2:
            return self.get(0, 0) * self.get(1, 1) - self.get(0, 1) * self.get(1, 0)
        if n == 3:
            a, b, c = self.get(0, 0), self.get(0, 1), self.get(0, 2)
            d, e, f = self.get(1, 0), self.get(1, 1), self.get(1, 2)
            g, h, i = self.get(2, 0), self.get(2, 1), self.get(2, 2)
            return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)

        # Gaussian elimination for n > 3
        mat = [list(self.data[i * n:(i + 1) * n]) for i in range(n)]
        d = 1.0
        for col in range(n):
            pivot = col
            for row in range(col + 1, n):
                if abs(mat[row][col]) > abs(mat[pivot][col]):
                    pivot = row
            if abs(mat[pivot][col]) < 1e-12:
                return 0.0
            if pivot != col:
                mat[col], mat[pivot] = mat[pivot], mat[col]
                d = -d
            d *= mat[col][col]
            for row in range(col + 1, n):
                factor = mat[row][col] / mat[col][col]
                for k in range(col, n):
                    mat[row][k] -= factor * mat[col][k]
        return d

    def __repr__(self):
        row_strs = []
        for r in range(self.rows):
            row_vals = [f"{int(x)}" if x == int(x) else f"{x:.4g}" for x in [self.get(r, c) for c in range(self.cols)]]
            row_strs.append(", ".join(row_vals))
        return "[" + " ; ".join(row_strs) + "]"


class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.vars: Dict[str, Any] = {}

    def get(self, name: str) -> Any:
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Hawk NameError: Undefined variable '{name}'")

    def set(self, name: str, val: Any):
        curr = self
        while curr:
            if name in curr.vars:
                curr.vars[name] = val
                return
            curr = curr.parent
        self.vars[name] = val

    def assign_existing(self, name: str, val: Any) -> bool:
        if name in self.vars:
            self.vars[name] = val
            return True
        if self.parent:
            return self.parent.assign_existing(name, val)
        return False


class Interpreter:
    def __init__(self, print_func=print, input_func=input, current_file: Optional[str] = None):
        self.print_func = print_func
        self.input_func = input_func
        self.current_file = os.path.abspath(current_file) if current_file else None
        self.imported_files: Set[str] = set()
        if self.current_file:
            self.imported_files.add(os.path.realpath(self.current_file))
        self.globals = Environment()
        self.functions: Dict[str, FnDef] = {}
        self._init_builtins()

    def _init_builtins(self):
        self.globals.set("pi", math.pi)
        self.globals.set("e", math.e)

    def run(self, stmts: List[Stmt]) -> Any:
        try:
            return self.exec_block(stmts, self.globals)
        except ReturnSignal as r:
            return r.value
        except KeyboardInterrupt:
            print("")
            raise SystemExit(130)

    def exec_block(self, stmts: List[Stmt], env: Environment) -> Any:
        res = None
        for s in stmts:
            res = self.exec_stmt(s, env)
        return res

    def exec_stmt(self, stmt: Stmt, env: Environment) -> Any:
        if isinstance(stmt, SetStmt):
            val = self.eval_expr(stmt.value, env)
            env.set(stmt.name, val)
            return val

        if isinstance(stmt, IndexAssignStmt):
            m = env.get(stmt.matrix_name)
            if not isinstance(m, HawkMatrix):
                raise TypeError(f"Hawk TypeError: '{stmt.matrix_name}' is not a matrix!")
            r = int(self.eval_expr(stmt.row, env))
            c = int(self.eval_expr(stmt.column, env)) if stmt.column else 0
            val = float(self.eval_expr(stmt.value, env))
            m.set(r, c, val)
            return val

        if isinstance(stmt, PrintStmt):
            parts = []
            for e in stmt.expressions:
                val = self.eval_expr(e, env)
                if isinstance(val, bool):
                    parts.append("true" if val else "false")
                elif isinstance(val, float) and val == int(val):
                    parts.append(str(int(val)))
                else:
                    parts.append(str(val))
            self.print_func(*parts)
            return None

        if isinstance(stmt, FnDef):
            self.functions[stmt.name] = stmt
            return None

        if isinstance(stmt, ReturnStmt):
            val = self.eval_expr(stmt.value, env) if stmt.value else None
            raise ReturnSignal(val)

        if isinstance(stmt, IfStmt):
            cond = self.eval_expr(stmt.condition, env)
            if cond:
                return self.exec_block(stmt.then_body, Environment(env))
            elif stmt.else_body:
                return self.exec_block(stmt.else_body, Environment(env))
            return None

        if isinstance(stmt, WhileStmt):
            while self.eval_expr(stmt.condition, env):
                self.exec_block(stmt.body, Environment(env))
            return None

        if isinstance(stmt, ForStmt):
            loop_env = Environment(env)
            if stmt.init:
                self.exec_stmt(stmt.init, loop_env)
            while stmt.condition is None or self.eval_expr(stmt.condition, loop_env):
                self.exec_block(stmt.body, Environment(loop_env))
                if stmt.step:
                    self.exec_stmt(stmt.step, loop_env)
            return None

        if isinstance(stmt, ExprStmt):
            return self.eval_expr(stmt.expr, env)

        if isinstance(stmt, ImportStmt):
            return self.exec_import(stmt, env)

        return None

    def exec_import(self, stmt: ImportStmt, env: Environment) -> Any:
        base_dir = os.path.dirname(self.current_file) if self.current_file else os.getcwd()
        raw_path = stmt.module_path

        def _find_module(path: str, base: str) -> Optional[str]:
            """Search for a .hwk module in: local dir -> bundled stdlib -> user stdlib."""
            # 1. Local (relative to current script)
            c = os.path.normpath(os.path.join(base, path))
            if os.path.exists(c):
                return c
            if not path.endswith(".hwk"):
                c_hwk = c + ".hwk"
                if os.path.exists(c_hwk):
                    return c_hwk
            # 2. Bundled stdlib next to hawk package
            pkg_dir = os.path.dirname(os.path.abspath(__file__))
            for stdlib_dir in [
                os.path.join(pkg_dir, "stdlib"),
                os.path.join(os.path.expanduser("~"), ".pyhawk", "stdlib"),
            ]:
                c = os.path.normpath(os.path.join(stdlib_dir, path))
                if os.path.exists(c):
                    return c
                if not path.endswith(".hwk"):
                    c_hwk = c + ".hwk"
                    if os.path.exists(c_hwk):
                        return c_hwk
            return None

        candidate = _find_module(raw_path, base_dir)
        if not candidate:
            raise FileNotFoundError(
                f"Hawk Error: Cannot import '{raw_path}'. "
                f"File not found in local dir, hawk/stdlib/, or ~/.pyhawk/stdlib/."
            )

        real_path = os.path.realpath(candidate)
        if real_path in self.imported_files:
            return None

        self.imported_files.add(real_path)

        with open(real_path, "r", encoding="utf-8") as f:
            code = f.read()

        from hawk.lexer import Lexer
        from hawk.parser import Parser
        tokens = Lexer(code).tokenize()
        imported_ast = Parser(tokens).parse()

        prev_file = self.current_file
        self.current_file = real_path
        try:
            self.exec_block(imported_ast, env)
        finally:
            self.current_file = prev_file
        return None

    def eval_expr(self, expr: Expr, env: Environment) -> Any:
        if isinstance(expr, NumberExpr):
            return expr.value

        if isinstance(expr, StringExpr):
            # Simple f-string interpolation {expr}
            s = expr.value
            if "{" in s and "}" in s:
                import re
                def repl(match):
                    var_name = match.group(1).strip()
                    try:
                        v = env.get(var_name)
                        if isinstance(v, float) and v == int(v):
                            return str(int(v))
                        return str(v)
                    except Exception:
                        return match.group(0)
                s = re.sub(r"\{([^}]+)\}", repl, s)
            return s

        if isinstance(expr, BoolExpr):
            return expr.value

        if isinstance(expr, VarExpr):
            return env.get(expr.name)

        if isinstance(expr, MatrixLiteral):
            rows_data = []
            cols_count = -1
            flat_data = []
            for r in expr.rows:
                row_vals = [float(self.eval_expr(e, env)) for e in r]
                if cols_count == -1:
                    cols_count = len(row_vals)
                elif cols_count != len(row_vals):
                    raise ValueError(f"Hawk MatrixError: Jagged matrix rows (expected {cols_count} elements, got {len(row_vals)})")
                flat_data.extend(row_vals)
            rows_count = len(expr.rows)
            return HawkMatrix(rows=rows_count, cols=cols_count if cols_count != -1 else 0, data=flat_data)

        if isinstance(expr, MatrixIndexExpr):
            m = self.eval_expr(expr.matrix, env)
            if not isinstance(m, HawkMatrix):
                raise TypeError("Hawk TypeError: Matrix indexing [r, c] is only applicable to matrices")
            r = int(self.eval_expr(expr.row, env))
            c = int(self.eval_expr(expr.column, env)) if expr.column else 0
            return m.get(r, c)

        if isinstance(expr, TransposeExpr):
            m = self.eval_expr(expr.matrix, env)
            if isinstance(m, HawkMatrix):
                return m.transpose()
            raise TypeError("Hawk TypeError: Transpose operator ' is only applicable to matrices")

        if isinstance(expr, UnaryOpExpr):
            op = self.eval_expr(expr.operand, env)
            if expr.op == "-":
                if isinstance(op, HawkMatrix):
                    return op.mult(-1.0)
                return -op
            if expr.op == "not":
                return not op

        if isinstance(expr, BinOpExpr):
            l = self.eval_expr(expr.left, env)
            r = self.eval_expr(expr.right, env)

            op = expr.op
            if op == "+":
                if isinstance(l, HawkMatrix) and isinstance(r, HawkMatrix):
                    return l.add(r)
                if isinstance(l, str) or isinstance(r, str):
                    return str(l) + str(r)
                return l + r
            if op == "-":
                if isinstance(l, HawkMatrix) and isinstance(r, HawkMatrix):
                    return l.sub(r)
                return l - r
            if op == "*":
                if isinstance(l, HawkMatrix) or isinstance(r, HawkMatrix):
                    if isinstance(l, HawkMatrix):
                        return l.mult(r)
                    return r.mult(l)
                if isinstance(l, str) or isinstance(r, str):
                    raise TypeError("Hawk TypeError: Cannot multiply strings! To print multiple values, separate them with commas: print \"Hello\", name")
                return l * r
            if op == "/":
                if r == 0:
                    raise ZeroDivisionError("Hawk Error: Division by zero")
                return l / r
            if op == "%":
                if r == 0:
                    raise ZeroDivisionError("Hawk Error: Division or modulo by zero")
                return l % r
            if op == "^":
                return l ** r

            # Comparisons
            if op == "=":  # Equality!
                if isinstance(l, HawkMatrix) and isinstance(r, HawkMatrix):
                    return l.rows == r.rows and l.cols == r.cols and l.data == r.data
                return l == r
            if op == "!=":
                return l != r
            if op == ">":
                return l > r
            if op == "<":
                return l < r
            if op == ">=":
                return l >= r
            if op == "<=":
                return l <= r
            if op == "and":
                return l and r
            if op == "or":
                return l or r

        if isinstance(expr, CallExpr):
            args = [self.eval_expr(a, env) for a in expr.args]

            # Built-in functions
            if expr.callee == "det":
                if isinstance(args[0], HawkMatrix):
                    return args[0].det()
                raise TypeError("Hawk TypeError: det() requires a matrix")
            if expr.callee == "sin": return math.sin(args[0])
            if expr.callee == "cos": return math.cos(args[0])
            if expr.callee == "tan": return math.tan(args[0])
            if expr.callee == "sqrt": return math.sqrt(args[0])
            if expr.callee == "abs": return abs(args[0])
            if expr.callee == "input":
                prompt = args[0] if args else ""
                raw = self.input_func(str(prompt))
                try:
                    return float(raw)
                except ValueError:
                    return raw

            if expr.callee == "system":
                cmd = str(args[0]) if args else ""
                return float(os.system(cmd))

            if expr.callee == "shell_output":
                # Run a shell command and return its stdout as a string
                cmd = str(args[0]) if args else ""
                try:
                    result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
                    return result.strip()
                except subprocess.CalledProcessError as e:
                    return (e.output or "").strip()

            if expr.callee == "typeof":
                # Return the type of a value as a string
                if not args:
                    return "null"
                val = args[0]
                if isinstance(val, HawkMatrix):
                    return "matrix"
                if isinstance(val, bool):
                    return "boolean"
                if isinstance(val, (int, float)):
                    return "number"
                if isinstance(val, str):
                    return "string"
                return "unknown"

            if expr.callee == "os_name":
                if sys.platform.startswith("darwin"):
                    return "macos"
                elif sys.platform.startswith("win"):
                    return "windows"
                else:
                    return "linux"

            if expr.callee == "chdir":
                path = str(args[0]) if args else ""
                try:
                    os.chdir(path)
                    return 0.0
                except OSError:
                    return -1.0

            if expr.callee == "beep":
                if sys.platform.startswith("win"):
                    try:
                        import winsound
                        winsound.MessageBeep()
                    except Exception:
                        print("\a", end="", flush=True)
                else:
                    print("\a", end="", flush=True)
                return None

            if expr.callee == "play_sound":
                path = str(args[0]) if args else ""
                if sys.platform.startswith("darwin"):
                    subprocess.Popen(["afplay", path],
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)
                elif sys.platform.startswith("win"):
                    try:
                        import winsound
                        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    except Exception:
                        pass
                else:
                    # Linux: try paplay, then aplay, then play (sox)
                    for player in ["paplay", "aplay", "play"]:
                        try:
                            subprocess.Popen([player, path],
                                             stdout=subprocess.DEVNULL,
                                             stderr=subprocess.DEVNULL)
                            break
                        except FileNotFoundError:
                            continue
                return None

            # User-defined functions
            if expr.callee in self.functions:
                fn_def = self.functions[expr.callee]
                if len(args) != len(fn_def.params):
                    raise TypeError(f"Hawk TypeError: Function '{expr.callee}' expects {len(fn_def.params)} arguments, got {len(args)}")
                call_env = Environment(self.globals)
                for p_name, arg_val in zip(fn_def.params, args):
                    call_env.set(p_name, arg_val)
                try:
                    return self.exec_block(fn_def.body, call_env)
                except ReturnSignal as ret:
                    return ret.value

            raise NameError(f"Hawk NameError: Undefined function '{expr.callee}'")

        raise NotImplementedError(f"Hawk Error: Unknown expression type: {type(expr)}")
