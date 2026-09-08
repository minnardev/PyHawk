#!/usr/bin/env python3
"""
PyHawk Programming Language — CLI
«Sharp as a hawk, fast as math»
"""

import sys
import os
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from hawk.lexer import Lexer
from hawk.parser import Parser
from hawk.interpreter import Interpreter
from hawk.transpiler import CTranspiler

HAWK_LOGO = r"""
     __   __  _______  _     _  ___   _ 
    |  | |  ||   _   || | _ | ||   | | |
    |  |_|  ||  |_|  || || || ||   |_| |
    |       ||       ||       ||      _|
    |       ||       ||       ||     |_ 
    |   _   ||   _   ||   _   ||    _  |
    |__| |__||__| |__||__| |__||___| |_|
   PyHawk — Sharp as a hawk, fast as math (v0.1)
"""


def cmd_run(args):
    filepath = args.file
    if not os.path.exists(filepath):
        print(f"Hawk Error: File '{filepath}' not found!")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        interp = Interpreter(current_file=os.path.abspath(filepath))
        interp.run(ast)
    except Exception as e:
        print(f"{e}")
        sys.exit(1)


def cmd_build(args):
    filepath = args.file
    if not os.path.exists(filepath):
        print(f"Hawk Error: File '{filepath}' not found!")
        sys.exit(1)

    output_path = args.output
    if not output_path:
        base_name = os.path.splitext(filepath)[0]
        output_path = base_name

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        print(f"Compiling '{os.path.basename(filepath)}' to native binary...")
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        transpiler = CTranspiler()
        bin_file = transpiler.build_native(ast, os.path.abspath(output_path), current_file=os.path.abspath(filepath))
        print(f"Successfully compiled to '{bin_file}'!")
        print(f"   Run: ./{os.path.basename(bin_file)}")
    except Exception as e:
        print(f"{e}")
        sys.exit(1)


def cmd_emit(args):
    filepath = args.file
    if not os.path.exists(filepath):
        print(f"Hawk Error: File '{filepath}' not found!")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        transpiler = CTranspiler()
        c_code = transpiler.transpile(ast, current_file=os.path.abspath(filepath))
        print(c_code)
    except Exception as e:
        print(f"{e}")
        sys.exit(1)


def cmd_repl(args):
    print(HAWK_LOGO)
    print("Interactive Hawk Console. Exit: 'exit' or Ctrl+C")
    print("Example: set m = [1, 2 ; 3, 4]  ->  m * m'")
    print("-" * 55)

    interp = Interpreter()

    while True:
        try:
            line = input("hawk> ").strip()
            if not line:
                continue
            if line in ("exit", "quit"):
                print("Goodbye!")
                break

            # If an expression was typed without print/set, wrap in print for REPL
            if not (line.startswith("set ") or line.startswith("print ") or line.startswith("fn ") or
                    line.startswith("if ") or line.startswith("while ") or line.startswith("for ")):
                test_code = f"print {line}"
            else:
                test_code = line

            tokens = Lexer(test_code).tokenize()
            ast = Parser(tokens).parse()
            interp.run(ast)

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Hawk Error: {e}")


def cmd_check(args):
    import json
    if args.stdin:
        code = sys.stdin.read()
    else:
        if not args.file or not os.path.exists(args.file):
            print(json.dumps([{"line": 1, "col": 1, "end_col": 5, "message": f"File '{args.file}' not found", "severity": "error"}]))
            return
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()

    from hawk.diagnostics import analyze
    diags = analyze(code)
    print(json.dumps(diags, ensure_ascii=False))


def cmd_format(args):
    from hawk.formatter import format_code
    if args.stdin:
        code = sys.stdin.read()
        formatted = format_code(code)
        sys.stdout.write(formatted)
    else:
        if not args.file or not os.path.exists(args.file):
            print(f"Hawk Error: File '{args.file}' not found!")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()
        formatted = format_code(code)
        if args.write:
            with open(args.file, "w", encoding="utf-8") as f:
                f.write(formatted)
            print(f"Formatted '{args.file}'")
        else:
            sys.stdout.write(formatted)


def main():
    parser = argparse.ArgumentParser(
        description="PyHawk Programming Language — CLI (\"Sharp as a hawk, fast as math\")"
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Command to execute")

    # run
    p_run = subparsers.add_parser("run", help="Run Hawk file via interpreter")
    p_run.add_argument("file", help="Path to .hwk file")

    # build
    p_build = subparsers.add_parser("build", help="Compile to native binary (C99 + clang -O3)")
    p_build.add_argument("file", help="Path to .hwk file")
    p_build.add_argument("-o", "--output", help="Output binary path")

    # emit
    p_emit = subparsers.add_parser("emit", help="Show generated clean C code")
    p_emit.add_argument("file", help="Path to .hwk file")

    # repl
    subparsers.add_parser("repl", help="Interactive REPL console")

    # check
    p_check = subparsers.add_parser("check", help="Check syntax and output JSON diagnostics")
    p_check.add_argument("file", nargs="?", default=None, help="Path to .hwk file")
    p_check.add_argument("--stdin", action="store_true", help="Read code from standard input")

    # format
    p_format = subparsers.add_parser("format", help="Format Hawk source code")
    p_format.add_argument("file", nargs="?", default=None, help="Path to .hwk file")
    p_format.add_argument("-w", "--write", action="store_true", help="Format and overwrite file in-place")
    p_format.add_argument("--stdin", action="store_true", help="Read code from stdin and output formatted code to stdout")

    # version
    subparsers.add_parser("version", help="Print Hawk version")

    args = parser.parse_args()

    if args.subcommand == "run":
        cmd_run(args)
    elif args.subcommand == "build":
        cmd_build(args)
    elif args.subcommand == "emit":
        cmd_emit(args)
    elif args.subcommand == "repl":
        cmd_repl(args)
    elif args.subcommand == "check":
        cmd_check(args)
    elif args.subcommand == "format":
        cmd_format(args)
    elif args.subcommand == "version":
        print("PyHawk v0.3.1")
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")  # clean newline after ^C
        raise SystemExit(130)
