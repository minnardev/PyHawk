# 🦅 PyHawk Programming Language

<p align="center">
  <img src="https://img.shields.io/badge/Language-PyHawk%20v0.1-blue.svg" alt="PyHawk" />
  <img src="https://img.shields.io/badge/Backend-Native%20C%20%2B%20Clang-green.svg" alt="Backend" />
  <img src="https://img.shields.io/badge/Matrices-In%20Core%20Syntax-orange.svg" alt="Matrices" />
  <img src="https://img.shields.io/badge/Platforms-macOS%20%7C%20Linux%20%7C%20Windows-brightgreen.svg" alt="Platforms" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License" />
</p>

```
     __   __  _______  _     _  ___   _ 
    |  | |  ||   _   || | _ | ||   | | |
    |  |_|  ||  |_|  || || || ||   |_| |
    |       ||       ||       ||      _|
    |       ||       ||       ||     |_ 
    |   _   ||   _   ||   _   ||    _  |
    |__| |__||__| |__||__| |__||___| |_|
   🦅 PyHawk — Sharp as a hawk, fast as math
```

> **PyHawk** — полнофункциональный прототип языка Hawk на Python с прямой трансляцией в машинный Си (C99 -O3).
> Создан для быстрой обкатки синтаксиса и тестирования фичей перед написанием компилятора на чистом Си.
> Файлы исходного кода: `.hwk`

---

## ⚡ Быстрая установка (Installer)

### macOS / Linux:
```bash
./install.sh
```
*(Скрипт автоматически добавит `pyhawk` и `hawk` в `~/.local/bin`, настроит `$PATH` в твоём шелле и установит расширение для VS Code).*

### Windows:
Запустите `install.bat` (или в PowerShell: `powershell -ExecutionPolicy Bypass -File install.ps1`).
*(Автоматически добавит `pyhawk` в системный PATH и установит расширение).*

### Установка через pip (любая ОС):
```bash
pip install -e .
```

## 🎯 Манифест и Философия

Hawk — **НЕ** узкоспециализированный математический калькулятор. Это язык для:
- ⚡ Сложных математических подсчётов **на лету** (киллер-фича).
- 💻 Обычных системных программ и утилит.
- 🌐 Серверов и Telegram-ботов.

**Родословная:** Python (чистота и читаемость) + C (скорость, структуры) + MATLAB (матрицы в ядре).

---

## 📐 Синтаксис

### 1. Переменные только через `set`
```hwk
set x = 5
set pi = 3.14159
set name = "Ястреб"
set r: float = 5.0    # опциональная аннотация типа
```
> 💡 В Hawk знак `=` внутри выражений используется **только для проверки равенства** (как в математике и SQL). Присваивание происходит только через `set`. Голое присвоение `x = 5` выдаёт понятную подсказку.

### 2. Матрицы в синтаксисе ядра (стиль MATLAB)
Точка с запятой `;` живёт **только внутри матриц** и разделяет строки:
```hwk
set A = [1, 2 ; 3, 4]
set B = [2, 0 ; 1, 2]

set C = A * B         # матричное произведение
set At = A'           # транспонирование через штрих '
print det(A)          # определитель
print C[0, 1]         # взятие элемента [строка, столбец]
```

### 3. Математические сокращения (неявное умножение)
Hawk понимает математическую запись без лишних звездочек `*`:
```hwk
set S = pi r^2        # эквивалентно: pi * (r ^ 2)
set y = 2x + 1        # эквивалентно: 2 * x + 1
```

### 4. Функции (`fn` / `return`)
```hwk
fn area(r) {
    return pi r^2
}
print "Площадь r=5:", area(5)
```

### 5. Условия и циклы
```hwk
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
```

---

## ⚡️ Быстрый старт (CLI)

```bash
# Сделать удобный алиас (опционально)
alias hawk="python3 $(pwd)/hawk_cli.py"

# 1. Запустить интерактивный REPL:
python3 hawk_cli.py repl

# 2. Быстро выполнить скрипт через интерпретатор:
python3 hawk_cli.py run examples/identity.hwk

# 3. Посмотреть чистый C-код, который генерирует Hawk (идеально для изучения C!):
python3 hawk_cli.py emit examples/identity.hwk

# 4. Скомпилировать в НАСТОЯЩИЙ бинарный файл через clang -O3:
python3 hawk_cli.py build examples/identity.hwk -o my_app
./my_app
```

---

## 🧠 Архитектура: связь с языком C

Компилятор Hawk транслирует ваш код в чистый Си с подключением высокоскоростного заголовочного файла `hawk_matrix.h`:

```c
typedef struct {
    int rows;
    int cols;
    double *data;
} Matrix;
```

Каждая операция над матрицами (`A * B`, `A'`, `det(A)`) превращается в прямые обращения к плоскому массиву памяти `data[row * cols + col]`, обеспечивая максимальную скорость процессора.

---

## 🧪 Тесты

Запуск модульных тестов:
```bash
python3 test_hawk.py
```
```
test_c_native_compilation ... ok
test_chained_comparison ... ok
test_equality_operator ... ok
test_functions_and_loops ... ok
test_implicit_multiplication_and_math ... ok
test_matrix_operations ... ok
test_naked_assignment_error ... ok

Ran 7 tests in 0.490s
OK
```

---

## 🔓 Лицензия

Распространяется под лицензией **MIT**.
«Sharp as a hawk, fast as math». 🦅
