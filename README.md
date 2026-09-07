# PyHawk Programming Language

<p align="center">
  <img src="https://img.shields.io/badge/Language-PyHawk%20v0.3.1-blue.svg" alt="PyHawk" />
  <img src="https://img.shields.io/badge/Backend-Native%20C%20%2B%20Clang-green.svg" alt="Backend" />
  <img src="https://img.shields.io/badge/Matrices-In%20Core%20Syntax-orange.svg" alt="Matrices" />
  <img src="https://img.shields.io/badge/Modules-import%20system-purple.svg" alt="Modules" />
  <img src="https://img.shields.io/badge/Platforms-macOS%20%7C%20Linux%20%7C%20Windows-brightgreen.svg" alt="Platforms" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License" />
</p>

```text
     __   __  _______  _     _  ___   _ 
    |  | |  ||   _   || | _ | ||   | | |
    |  |_|  ||  |_|  || || || ||   |_| |
    |       ||       ||       ||      _|
    |       ||       ||       ||     |_ 
    |   _   ||   _   ||   _   ||    _  |
    |__| |__||__| |__||__| |__||___| |_|
   PyHawk — Sharp as a hawk, fast as math (v0.3.1)
```

> **PyHawk** is a full-featured programming language with mathematical syntax, clean code design, and direct translation into native C (C99 -O3 via Clang/GCC).  
> Source code files: `.hwk`

---

## Quick Installation

### macOS / Linux:
```bash
./install.sh
```
*(The script automatically adds `pyhawk` and `hawk` to `~/.local/bin`, updates `$PATH` in your shell, and installs the VS Code extension).*

### Windows:
Run `install.bat` (or in PowerShell: `powershell -ExecutionPolicy Bypass -File install.ps1`).  
*(Automatically adds `pyhawk` to system PATH and installs the extension).*

### Installation via pip into a project (Any OS):
```bash
pip install -e .
```

---

## Manifesto & Philosophy

Hawk is **NOT** a domain-specific calculator. It is a language built for:
- Complex mathematical calculations **on the fly** (killer feature).
- Fast development of application scripts and system utilities.
- Structuring projects into clean multi-file modules (`import`).
- Servers and network services.

**Lineage:** Python (cleanliness and readability) + C (speed, native compilation) + MATLAB (matrices built into core syntax).

---

## Language Syntax

### 1. Variables require `set`
```hawk
set x = 5
set pi = 3.14159
set name = "Hawk"
set r: float = 5.0    # optional type annotation
```
> In Hawk, the `=` sign inside expressions is used **strictly for equality checks** (as in mathematics and SQL). Assignment occurs only via the `set` keyword. Bare assignment like `x = 5` throws a clear hint with line and column numbers.

### 2. Booleans (`true` / `false`) and Logic (`and`, `or`, `not`)
```hawk
set is_active = true
set is_admin = false

set can_access = is_active and (not is_admin or x > 0)

if (is_active = true) {
    print "System active"
}
```

### 3. Math, Implicit Multiplication & Modulo (`%`)
Hawk supports natural mathematical notation without unnecessary asterisks `*`:
```hawk
set S = pi r^2        # equivalent to: pi * (r ^ 2)
set y = 2x + 1        # equivalent to: 2 * x + 1

# Modulo (%)
set remainder = 10 % 3
print remainder       # prints: 1

fn is_even(n) {
    return (n % 2 = 0)
}
print is_even(4)      # true
print is_even(7)      # false
```

### 4. Interactive Input (`input`)
The `input("prompt: ")` function automatically handles types: numeric input parses as a number, text stays a string. Works identically in both the interpreter and compiled C binaries:
```hawk
set name = input("What's your name? ")
print "Hello,", name

set a = input("Enter first number: ")
set b = input("Enter second number: ")
print "Sum:", a + b
```

### 5. Multi-file Modules (`import`)
Hawk lets you build applications across multiple files easily. All functions and variables from an imported file are directly accessible:

**`helpers.hwk`**:
```hawk
fn square(x) {
    return x^2
}

set DEFAULT_OFFSET = 100
```

**`main.hwk`**:
```hawk
import "helpers.hwk"    # also supports: import "helpers" and import helpers

set val = 5
print square(val) + DEFAULT_OFFSET   # prints: 125
```
> The compiler automatically tracks circular dependencies and duplicate includes (similar to `#pragma once`), bundling modules into a single high-speed binary without linker issues.

### 6. Core Matrix Syntax (MATLAB-style)
Semicolons `;` exist **exclusively inside matrices** to separate rows:
```hawk
set A = [1, 2 ; 3, 4]
set B = [2, 0 ; 1, 2]

set C = A * B         # matrix multiplication
set At = A'           # transposition via prime operator '
print det(A)          # determinant
print C[0, 1]         # element access [row, column]
```

### 7. Functions (`fn` / `return`)
```hawk
fn area(r) {
    return pi r^2
}
print "Area r=5:", area(5)
```

### 8. Conditions and Loops
Chained comparisons work just like in mathematics:
```hawk
if (1 < r < 10) {
    print "r is strictly between 1 and 10!"
}

if (x = 5) {
    print "x equals 5!"
} else {
    print "x does not equal 5"
}

set count = 3
while (count > 0) {
    print count
    set count = count - 1
}

for (set i = 0; i < 5; set i = i + 1) {
    print "Step:", i
}
```

---

## Code Formatter (`format`)

PyHawk comes with a built-in code auto-formatter (4-space indentation, formatting for curly braces `{ ... }` and matrices `[ ... ]`, empty line normalization):

```bash
# Format file in-place:
pyhawk format script.hwk -w

# Output formatted code to stdout:
pyhawk format script.hwk

# Format via stdin:
cat script.hwk | pyhawk format --stdin
```

---

## VS Code Extension

The official extension is located in the `vscode-hawk/` directory:
- **Syntax Highlighting**: Keywords, matrices, functions, operators, and string interpolation.
- **Document Auto-formatting**: Via hotkeys **`Shift + Option + F`** (macOS) / **`Shift + Alt + F`** (Windows/Linux) or on save (`formatOnSave`).
- **Syntax Diagnostics (Linter)**: Real-time error highlighting and hints directly in the editor using `pyhawk check`.

---

## CLI Commands (`pyhawk` / `hawk`)

```bash
# 1. Launch interactive math REPL:
pyhawk repl

# 2. Execute a file via interpreter:
pyhawk run main.hwk

# 3. Compile to native binary (C99 + Clang -O3):
pyhawk build main.hwk -o my_app
./my_app

# 4. Inspect generated clean C code:
pyhawk emit main.hwk

# 5. Check syntax (JSON diagnostics for IDEs):
pyhawk check main.hwk

# 6. Format file:
pyhawk format main.hwk -w

# 7. Print language version:
pyhawk version
```

---

## Architecture: Native C Integration

The compiler translates Hawk code into strict ANSI C99 linked against the `hawk_matrix.h` runtime:
- Matrix operations work directly on flat arrays `data[r * cols + c]` without extra allocations.
- Dynamic operations and input routines are backed by a lightweight `HawkVal` engine.
- All imported modules compile into a single translation unit — producing a final binary built with `-O3` optimizations running at bare-metal speeds.

---

## Tests

Run the full unit test suite:
```bash
python3 test_hawk.py
```
```text
test_booleans_and_comparisons ... ok
test_c_native_compilation ... ok
test_c_native_dynamic_types_and_calculator ... ok
test_chained_comparison ... ok
test_circular_and_identifier_import ... ok
test_equality_operator ... ok
test_formatter ... ok
test_functions_and_loops ... ok
test_implicit_multiplication_and_math ... ok
test_import_multi_file ... ok
test_matrix_operations ... ok
test_modulo_operator ... ok
test_naked_assignment_error ... ok

----------------------------------------------------------------------
Ran 13 tests in 2.411s
OK
```

---

## License

Distributed under the open-source **MIT** license.  
"Sharp as a hawk, fast as math".
