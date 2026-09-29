# `random.hwk` — случайные числа

Все функции являются built-ins и не требуют подключения модуля.

```
hawk

import random

set n = rand_int(1, 100)
set f = rand_float()
print rand_float_range(1.0, 10.0)
```

| **Функция** | **Описание** |
| --- | --- |
| `rand_float()` | Случайное число от 0 до 1 |
| `rand_int(lo, hi)` | Случайное целое в диапазоне |
| `rand_float_range(lo, hi)` | Случайное float в диапазоне |
| `rand_int_range(lo, hi)` | Алиас для `rand_int` |
| `seed(s)` | Установить seed для ГПСЧ |
