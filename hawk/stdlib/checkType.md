# `checkType.hwk` — проверка типов

Работает поверх встроенной `typeof()`. Возвращает строку: `"number"`, `"string"`, `"boolean"`, `"matrix"`, `"null"`.

```
hawk

import checkType

set x = 42
set name = "Hawk"

print type_of(x)
print is_number(x)
print is_string(name)

if (not check_type(x, "string")) {
    print "x не является строкой"
}
```

| **Функция** | **Что делает** |
| --- | --- |
| `type_of(x)` | Возвращает тип как строку |
| `is_number(x)` | `true`, если x — число |
| `is_string(x)` | `true`, если x — строка |
| `is_bool(x)` | `true`, если x — логический тип |
| `is_matrix(x)` | `true`, если x — матрица |
| `is_null(x)` | `true`, если x — `null` / не определено |
| `check_type(x, expected)` | Печатает ошибку, если тип не совпал; возвращает `true` / `false` |
