"""
Тестовый набор для языка программирования Hawk v0.1
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

    def test_c_native_dynamic_types_and_calculator(self):
        code = """
        set a = 10
        set b = 5
        set c = "+"
        set done = false
        if (c = "+") {
            print a + b
            set done = true
        }
        if (c = "*") {
            print a * b
            set done = true
        }
        if (done = false) {
            print "Fail"
        }
        """
        out = self.build_and_run_native(code)
        self.assertEqual(out, ["15"])

    def test_import_multi_file(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            helper_path = os.path.join(tmpdir, "helpers.hwk")
            with open(helper_path, "w", encoding="utf-8") as f:
                f.write("""
                fn calc_double(x) {
                    return 2x
                }
                set CONST_OFFSET = 100
                """)

            main_path = os.path.join(tmpdir, "main.hwk")
            with open(main_path, "w", encoding="utf-8") as f:
                f.write("""
                import "helpers.hwk"
                set res = calc_double(21) + CONST_OFFSET
                print res
                """)

            # 1. Test Interpreter
            with open(main_path, "r", encoding="utf-8") as f:
                code_main = f.read()
            tokens = Lexer(code_main).tokenize()
            ast = Parser(tokens).parse()
            output = []
            interp = Interpreter(print_func=lambda *args: output.append(" ".join(str(a) for a in args)),
                                 current_file=main_path)
            interp.run(ast)
            self.assertEqual(output, ["142"])

            # 2. Test Native Compilation
            transpiler = CTranspiler()
            bin_path = os.path.join(tmpdir, "main_bin")
            transpiler.build_native(ast, bin_path, current_file=main_path)
            res = subprocess.run([bin_path], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)
            self.assertEqual(res.stdout.strip(), "142")

    def test_circular_and_identifier_import(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            file_b = os.path.join(tmpdir, "module_b.hwk")
            file_a = os.path.join(tmpdir, "module_a.hwk")

            with open(file_b, "w", encoding="utf-8") as f:
                f.write("""
                import module_a
                fn func_b() {
                    return 42
                }
                """)

            with open(file_a, "w", encoding="utf-8") as f:
                f.write("""
                import module_b
                print func_b()
                """)

            # Test interpreter doesn't crash in circular import and identifier syntax works
            with open(file_a, "r", encoding="utf-8") as f:
                code_a = f.read()
            tokens = Lexer(code_a).tokenize()
            ast = Parser(tokens).parse()
            output = []
            interp = Interpreter(print_func=lambda *args: output.append(" ".join(str(a) for a in args)),
                                 current_file=file_a)
            interp.run(ast)
            self.assertEqual(output, ["42"])

            # Test native compiler
            transpiler = CTranspiler()
            bin_path = os.path.join(tmpdir, "circ_bin")
            transpiler.build_native(ast, bin_path, current_file=file_a)
            res = subprocess.run([bin_path], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)
            self.assertEqual(res.stdout.strip(), "42")


if __name__ == "__main__":
    unittest.main(verbosity=2)
