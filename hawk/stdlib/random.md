# `random.hwk` — случайные числа и выборка

```
hawk

import random

print rand_int(1, 100)         # 42
print rand_float()             # 0.73...
print rand_float_range(1.5, 3.5)
print choice("rock|paper|scissors")
print shuffle("a|b|c|d")
seed("myseed")
```

| **Функция** | **Что делает** |
| --- | --- |
| `rand_float()` | Случайное число `0.0 <= x < 1.0` |
| `rand_float_range(lo, hi)` | Случайное число в диапазоне |
| `rand_int(lo, hi)` | Случайное целое `lo <= x <= hi` |
| `rand_int_range(lo, hi)` | Синоним `rand_int` |
| `choice(list_str)` | Случайный элемент из строки через `|` |
| `shuffle(list_str)` | Перемешивает элементы, разделённые `|` |
| `seed(s)` | Устанавливает seed для повторяемости |

**Важно:** `choice` и `shuffle` принимают список как строку с разделителем `|`, например `"a|b|c"`.
