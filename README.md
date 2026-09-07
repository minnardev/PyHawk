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
   PyHawk — Sharp as a hawk, fast as math (v0.1)
```

> **PyHawk** — полнофункциональный язык программирования с математическим синтаксисом, чистым кодом и прямой трансляцией в нативный машинный Си (C99 -O3 через Clang/GCC).
> Файлы исходного кода: `.hwk`

---

## Быстрая установка

### macOS / Linux:
```bash
./install.sh
```
*(Скрипт автоматически добавит `pyhawk` и `hawk` в `~/.local/bin`, настроит `$PATH` в вашем шелле и установит расширение для VS Code).*

### Windows:
Запустите `install.bat` (или в PowerShell: `powershell -ExecutionPolicy Bypass -File install.ps1`).
*(Автоматически добавит `pyhawk` в системный PATH и установит расширение).*

### Установка через pip (любая ОС):
```bash
pip install -e .
```

---

## Манифест и Философия

Hawk — **НЕ** узкоспециализированный калькулятор. Это язык для:
- Сложных математических подсчётов **на лету** (киллер-фича).
- Быстрой разработки прикладных скриптов и системных утилит.
- Разделения проектов на чистые многофайловые модули (`import`).
- Серверов и сетевых сервисов.

**Родословная:** Python (чистота и читаемость) + C (скорость, компиляция в машинный код) + MATLAB (матрицы в ядре синтаксиса).

---

## Синтаксис языка

### 1. Переменные только через `set`
```hawk
set x = 5
set pi = 3.14159
set name = "Hawk"
set r: float = 5.0    # опциональная аннотация типа
```
> В Hawk знак `=` внутри выражений используется **только для проверки равенства** (как в математике и SQL). Присваивание происходит только через ключевое слово `set`. Голое присвоение `x = 5` выдаёт понятную подсказку с номером строки и столбца.

### 2. Булевы типы (`true` / `false`) и логика (`and`, `or`, `not`)
```hawk
set is_active = true
set is_admin = false

set can_access = is_active and (not is_admin or x > 0)

if (is_active = true) {
    print "Система активна"
}
```

### 3. Математика, неявное умножение и остаток от деления (`%`)
Hawk поддерживает естественную математическую запись без лишних звёздочек `*`:
```hawk
set S = pi r^2        # эквивалентно: pi * (r ^ 2)
set y = 2x + 1        # эквивалентно: 2 * x + 1

# Остаток от деления (%)
set remainder = 10 % 3
print remainder       # напечатает: 1

fn is_even(n) {
    return (n % 2 = 0)
}
print is_even(4)      # true
print is_even(7)      # false
```

### 4. Интерактивный ввод данных (`input`)
Функция `input("подсказка: ")` автоматически определяет тип: если введено число, оно становится числом, если текст — строкой. Работает одинаково как в интерпретаторе, так и в скомпилированном Си-бинарнике:
```hawk
set name = input("Как тебя зовут? ")
print "Привет,", name

set a = input("Введите первое число: ")
set b = input("Введите второе число: ")
print "Сумма:", a + b
```

### 5. Многофайловые модули (`import`)
Hawk позволяет легко собирать одно приложение из нескольких файлов. Все функции и переменные импортированного файла становятся напрямую доступны:

**`helpers.hwk`**:
```hawk
fn square(x) {
    return x^2
}

set DEFAULT_OFFSET = 100
```

**`main.hwk`**:
```hawk
import "helpers.hwk"    # также поддерживается: import "helpers" и import helpers

set val = 5
print square(val) + DEFAULT_OFFSET   # напечатает: 125
```
> Компилятор автоматически отслеживает циклические зависимости и повторные включения (аналог `#pragma once`), объединяя модули в единый высокоскоростной бинарник без проблем с линковкой.

### 6. Матрицы в синтаксисе ядра (стиль MATLAB)
Точка с запятой `;` живёт **только внутри матриц** и разделяет строки:
```hawk
set A = [1, 2 ; 3, 4]
set B = [2, 0 ; 1, 2]

set C = A * B         # матричное произведение
set At = A'           # транспонирование через штрих '
print det(A)          # определитель (детерминант)
print C[0, 1]         # взятие элемента [строка, столбец]
```

### 7. Функции (`fn` / `return`)
```hawk
fn area(r) {
    return pi r^2
}
print "Площадь r=5:", area(5)
```

### 8. Условия и циклы
Поддерживаются цепочечные сравнения как в математике:
```hawk
if (1 < r < 10) {
    print "r строго между 1 и 10!"
}

if (x = 5) {
    print "x равен 5!"
} else {
    print "x не равен 5"
}

set count = 3
while (count > 0) {
    print count
    set count = count - 1
}

for (set i = 0; i < 5; set i = i + 1) {
    print "Шаг:", i
}
```

---

## Форматтер кода (`format`)

PyHawk поставляется со встроенным автоформаттером кода (отступы 4 пробела, форматирование фигурных скобок `{ ... }` и матриц `[ ... ]`, нормализация пустых строк):

```bash
# Отформатировать файл на месте:
pyhawk format script.hwk -w

# Вывести отформатированный код в stdout:
pyhawk format script.hwk

# Форматирование через stdin:
cat script.hwk | pyhawk format --stdin
```

---

## Расширение для VS Code

В папке `vscode-hawk/` находится официальное расширение:
- **Подсветка синтаксиса**: ключевые слова, матрицы, функции, операторы и интерполяция строк.
- **Автоформатирование документа**: по горячим клавишам **`Shift + Option + F`** (macOS) / **`Shift + Alt + F`** (Windows/Linux) или при сохранении (`formatOnSave`).
- **Синтаксическая диагностика (Linter)**: мгновенная подсветка ошибок и подсказки прямо в редакторе через команду `pyhawk check`.

---

## Команды CLI (`pyhawk` / `hawk`)

```bash
# 1. Запустить интерактивную математическую консоль (REPL):
pyhawk repl

# 2. Выполнить файл через интерпретатор:
pyhawk run main.hwk

# 3. Скомпилировать в нативный бинарник (C99 + Clang -O3):
pyhawk build main.hwk -o my_app
./my_app

# 4. Посмотреть сгенерированный чистый код на Си:
pyhawk emit main.hwk

# 5. Проверить синтаксис (JSON-диагностика для IDE):
pyhawk check main.hwk

# 6. Отформатировать файл:
pyhawk format main.hwk -w

# 7. Версия языка:
pyhawk version
```

---

## Архитектура: связь с машинным Си

Компилятор транслирует код Hawk в строгий ANSI C99 с подключением рантайма `hawk_matrix.h`:
- Матричные операции работают напрямую с плоским массивом `data[r * cols + c]` без лишних аллокаций.
- Динамические операции и функции ввода поддерживаются через легковесную систему `HawkVal`.
- Все импортированные модули компилируются в единую единицу трансляции — итоговый бинарник компилируется с оптимизациями `-O3` и выполняется с максимальной скоростью процессора.

---

## Тесты

Запуск полного набора модульных тестов:
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

## Лицензия

Распространяется под свободной лицензией **MIT**.  
«Sharp as a hawk, fast as math».
