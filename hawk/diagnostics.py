"""
🦅 PyHawk Diagnostics & Linter Engine
Provides syntax error diagnostics in JSON format for VS Code.
"""

import re
from typing import List, Dict, Any, Tuple
from hawk.errors import HawkError, HawkSyntaxError
from hawk.lexer import Lexer
from hawk.parser import Parser


def _extract_line_col(msg: str) -> Tuple[int, int]:
    line = 1
    col = 1
    m_line = re.search(r'line\s*(\d+)', msg, re.I) or re.search(r'line\s*(\d+)', msg, re.I)
    if m_line:
        line = int(m_line.group(1))
    m_col = re.search(r'col(?:umn)?\s*(\d+)', msg, re.I) or re.search(r'col(?:umn)?\s*(\d+)', msg, re.I)
    if m_col:
        col = int(m_col.group(1))
    return line, col


def analyze(code: str) -> List[Dict[str, Any]]:
    diagnostics: List[Dict[str, Any]] = []

    # 1. Tokenization (Lexical analysis)
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
    except HawkError as e:
        diagnostics.append({
            "line": e.line,
            "col": e.col,
            "end_col": e.end_col,
            "message": e.raw_message,
            "severity": "error"
        })
        return diagnostics
    except SyntaxError as e:
        line, col = _extract_line_col(str(e))
        diagnostics.append({
            "line": line,
            "col": col,
            "end_col": col + 5,
            "message": str(e),
            "severity": "error"
        })
        return diagnostics
    except Exception as e:
        diagnostics.append({
            "line": 1,
            "col": 1,
            "end_col": 10,
            "message": str(e),
            "severity": "error"
        })
        return diagnostics

    # 2. Syntax analysis (AST parsing)
    try:
        parser = Parser(tokens)
        parser.parse()
    except HawkError as e:
        diagnostics.append({
            "line": e.line,
            "col": e.col,
            "end_col": e.end_col,
            "message": e.raw_message,
            "severity": "error"
        })
        return diagnostics
    except SyntaxError as e:
        line, col = _extract_line_col(str(e))
        diagnostics.append({
            "line": line,
            "col": col,
            "end_col": col + 5,
            "message": str(e),
            "severity": "error"
        })
        return diagnostics
    except Exception as e:
        diagnostics.append({
            "line": 1,
            "col": 1,
            "end_col": 10,
            "message": str(e),
            "severity": "error"
        })
        return diagnostics

    return diagnostics
