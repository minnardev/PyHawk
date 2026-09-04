"""
🦅 PyHawk Errors Definition
"""

from typing import Optional


class HawkError(Exception):
    def __init__(self, message: str, line: int = 1, col: int = 1, end_col: Optional[int] = None):
        self.raw_message = message
        self.line = line
        self.col = col
        self.end_col = end_col or (col + 1)
        super().__init__(f"Hawk Error (строка {line}, столбец {col}): {message}")


class HawkSyntaxError(HawkError, SyntaxError):
    pass
