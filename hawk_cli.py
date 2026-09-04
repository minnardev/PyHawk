#!/usr/bin/env python3
"""
🦅 PyHawk Programming Language — CLI
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
   🦅 PyHawk — Sharp as a hawk, fast as math (v0.1)
"""


def cmd_run(args):
    filepath = args.file
    if not os.path.exists(filepath):
        print(f"Hawk Error: Файл '{filepath}' не найден!")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        interp = Interpreter()
        interp.run(ast)
    except Exception as e:
        print(f"{e}")
        sys.exit(1)


def cmd_build(args):
    filepath = args.file
    if not os.path.exists(filepath):
        print(f"Hawk Error: Файл '{filepath}' не найден!")
        sys.exit(1)

    output_path = args.output
    if not output_path:
        base_name = os.path.splitext(filepath)[0]
        output_path = base_name

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        print(f"🦅 Компиляция '{os.path.basename(filepath)}' в нативный бинарник...")
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        transpiler = CTranspiler()
        bin_file = transpiler.build_native(ast, os.path.abspath(output_path))
        print(f"✅ Успешно скомпилировано в '{bin_file}'!")
        print(f"   Запуск: ./{os.path.basename(bin_file)}")
    except Exception as e:
        print(f"{e}")
        sys.exit(1)


def cmd_emit(args):
    filepath = args.file
    if not os.path.exists(filepath):
        print(f"Hawk Error: Файл '{filepath}' не найден!")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        transpiler = CTranspiler()
        c_code = transpiler.transpile(ast)
        print(c_code)
    except Exception as e:
        print(f"{e}")
        sys.exit(1)


def cmd_repl(args):
    print(HAWK_LOGO)
    print("Интерактивная консоль Hawk. Выход: 'exit' или Ctrl+C")
    print("Пример: set m = [1, 2 ; 3, 4]  ->  m * m'")
    print("-" * 55)

    interp = Interpreter()

    while True:
        try:
            line = input("🦅 hawk> ").strip()
            if not line:
                continue
            if line in ("exit", "quit"):
                print("До скорых встреч! 🦅")
                break

            # Если введено выражение без print/set, оборачиваем в print для REPL
            if not (line.startswith("set ") or line.startswith("print ") or line.startswith("fn ") or
                    line.startswith("if ") or line.startswith("while ") or line.startswith("for ")):
                test_code = f"print {line}"
            else:
                test_code = line

            tokens = Lexer(test_code).tokenize()
            ast = Parser(tokens).parse()
            interp.run(ast)

        except (KeyboardInterrupt, EOFError):
            print("\nДо скорых встреч! 🦅")
            break
        except Exception as e:
            print(f"Hawk Error: {e}")


def cmd_check(args):
    import json
    if args.stdin:
        code = sys.stdin.read()
    else:
        if not args.file or not os.path.exists(args.file):
            print(json.dumps([{"line": 1, "col": 1, "end_col": 5, "message": f"Файл '{args.file}' не найден", "severity": "error"}]))
            return
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()

    from hawk.diagnostics import analyze
    diags = analyze(code)
    print(json.dumps(diags, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="🦅 PyHawk Programming Language — CLI («Sharp as a hawk, fast as math»)"
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Команда для выполнения")

    # run
    p_run = subparsers.add_parser("run", help="Запустить файл через интерпретатор")
    p_run.add_argument("file", help="Путь к файлу .hwk")

    # build
    p_build = subparsers.add_parser("build", help="Скомпилировать в нативный бинарник (C99 + clang -O3)")
    p_build.add_argument("file", help="Путь к файлу .hwk")
    p_build.add_argument("-o", "--output", help="Имя выходного бинарника")

    # emit
    p_emit = subparsers.add_parser("emit", help="Показать сгенерированный чистый код на Си")
    p_emit.add_argument("file", help="Путь к файлу .hwk")

    # repl
    subparsers.add_parser("repl", help="Интерактивная консоль (REPL)")

    # check
    p_check = subparsers.add_parser("check", help="Проверка синтаксиса и вывод диагностик в JSON")
    p_check.add_argument("file", nargs="?", default=None, help="Путь к файлу .hwk")
    p_check.add_argument("--stdin", action="store_true", help="Читать код из стандартного ввода")

    # version
    subparsers.add_parser("version", help="Версия Hawk")

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
    elif args.subcommand == "version":
        print("🦅 PyHawk v0.1 (Python prototype) — Springfield-to-Native Edition")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
