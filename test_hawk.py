"""
🦅 Тестовый набор для языка программирования Hawk v0.1
"""

import os
import sys
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from hawk.lexer import Lexer, TokenType
from hawk.parser import Parser
from hawk.interpreter import Interpreter, HawkMatrix
from hawk.transpiler import CTranspiler


class TestHawk(unittest.TestCase):
    def run_hawk(self, code: str) -> list:
        output = []
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        interp = Interpreter(print_func=lambda *args: output.append(" ".join(str(a) for a in args)))
        interp.run(ast)
        return output

    def build_and_run_native(self, code: str) -> list:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        transpiler = CTranspiler()
        bin_path = "/tmp/hawk_test_bin"
        transpiler.build_native(ast, bin_path)
        res = subprocess.run([bin_path], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Native run error: {res.stderr}")
        return [line.strip() for line in res.stdout.strip().split("\n") if line.strip()]

    def test_implicit_multiplication_and_math(self):
        code = """
        set r = 5
        set S = pi r^2
        print S
        set y = 2r + 3
        print y
        """
        out = self.run_hawk(code)
        self.assertAlmostEqual(float(out[0]), 3.141592653589793 * 25)
        self.assertEqual(out[1], "13")

    def test_equality_operator(self):
        code = """
        set x = 10
        if (x = 10) {
            print "yes"
        } else {
            print "no"
        }
        if (x != 5) {
            print "not 5"
        }
        """
        out = self.run_hawk(code)
        self.assertEqual(out, ["yes", "not 5"])

    def test_naked_assignment_error(self):
        code = """
        x = 5
        """
        with self.assertRaises(SyntaxError) as ctx:
            tokens = Lexer(code).tokenize()
            Parser(tokens).parse()
        self.assertIn("requires 'set' keyword", str(ctx.exception))

    def test_modulo_operator(self):
        code = """
        print 10 % 3
        print 7 % 3
        set x = 14 % 5
        print x
        """
        out = self.run_hawk(code)
        self.assertEqual(out, ["1", "1", "4"])

    def test_booleans_and_comparisons(self):
        code = """
        set t = true
        set f = false
        print t, f

        set x = 10
        set is_ten = (x = 10)
        set is_less = (x <= 15)
        set is_greater = (x >= 20)
        print is_ten, is_less, is_greater

        fn is_even(n) {
            return (n % 2 = 0)
        }
        print is_even(4), is_even(7)
        """
        out = self.run_hawk(code)
        self.assertEqual(out[0], "true false")
        self.assertEqual(out[1], "true true false")
        self.assertEqual(out[2], "true false")

    def test_matrix_operations(self):
        code = """
        set A = [1, 2 ; 3, 4]
        set B = [2, 0 ; 1, 2]
        set C = A * B
        print C[0, 0], C[0, 1]
        print C[1, 0], C[1, 1]
        set At = A'
        print At[0, 1]
        print det(A)
        """
        out = self.run_hawk(code)
        self.assertEqual(out[0], "4 4")
        self.assertEqual(out[1], "10 8")
        self.assertEqual(out[2], "3")  # A'[0, 1] == A[1, 0] == 3
        self.assertEqual(out[3], "-2")

    def test_functions_and_loops(self):
        code = """
        fn double_it(n) {
            return 2n
        }
        print double_it(21)

        set sum = 0
        set i = 1
        while (i <= 4) {
            set sum = sum + i
            set i = i + 1
        }
        print sum
        """
        out = self.run_hawk(code)
        self.assertEqual(out, ["42", "10"])

    def test_chained_comparison(self):
        code = """
        set r = 5
        if (1 < r < 10) {
            print "between"
        }
        if (10 < r < 20) {
            print "wrong"
        } else {
            print "correct"
        }
        """
        out = self.run_hawk(code)
        self.assertEqual(out, ["between", "correct"])

    def test_c_native_compilation(self):
        code = """
        set a = 3
        set b = 4
        set c = sqrt(a^2 + b^2)
        print "Гипотенуза:", c

        set m = [1, 2 ; 3, 4]
        print "det:", det(m)

        set mod_val = 10 % 3
        print "mod:", mod_val

        set flag = true
        print "flag:", flag
        """
        out = self.build_and_run_native(code)
        self.assertTrue(any("Гипотенуза: 5" in line for line in out))
        self.assertTrue(any("det: -2" in line for line in out))
        self.assertTrue(any("mod: 1" in line for line in out))
        self.assertTrue(any("flag: true" in line for line in out))

    def test_formatter(self):
        from hawk.formatter import format_code
        messy_code = """
set a = input("Enter: ")

    if (a = 0) {
        print "Win"
    }
    else {
        print "Lose"
    }
        """
        formatted = format_code(messy_code)
        expected = 'set a = input("Enter: ")\n\nif (a = 0) {\n    print "Win"\n} else {\n    print "Lose"\n}\n'
        self.assertEqual(formatted, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
