# `strings.hwk` — строковые утилиты

Все функции являются built-ins и не требуют подключения модуля.

```
hawk

import strings

set text = "  Hello, Hawk!  "

print to_upper(text)       # HELLO, HAWK!
print to_lower(text)       #   hello, hawk!  
print trim(text)           # Hello, Hawk!

if (contains(text, "Hawk") = "true") {
    print "Found Hawk"
}

set parts = split("a,b,c", ",")
print parts                # a|b|c
print join("a|b|c", "-")   # a-b-c

print length(text)         # 16
```

| **Категория** | **Функция** | **Описание** |
| --- | --- | --- |
| **Регистр** | `to_upper(s)` | Верхний регистр |
| | `to_lower(s)` | Нижний регистр |
| | `capitalize(s)` | Первая буква заглавная |
| **Пробелы** | `trim(s)` | Удалить пробелы с обоих сторон |
| | `trim_left(s)` | Удалить пробелы слева |
| | `trim_right(s)` | Удалить пробелы справа |
| **Поиск** | `contains(text, sub)` | `"true"` / `"false"` |
| | `starts_with(text, prefix)` | `"true"` / `"false"` |
| | `ends_with(text, suffix)` | `"true"` / `"false"` |
| | `index_of(text, sub)` | Индекс первого вхождения (`-1` если нет) |
| | `last_index_of(text, sub)` | Индекс последнего вхождения |
| **Изменение** | `replace(text, old, new)` | Заменить подстроку |
| | `substring(text, start, end)` | Срез [start:end) |
| | `slice(text, start)` | Срез от start до конца |
| | `slice_end(text, end)` | Срез от начала до end |
| | `repeat(text, count)` | Повторить строку |
| | `reverse(s)` | Реверс строки |
| | `pad_left(text, width, char)` | Дополнить слева |
| | `pad_right(text, width, char)` | Дополнить справа |
| **Разделение** | `split(text, sep)` | Разбить на части через `|` |
| | `join(parts, sep)` | Объединить части через разделитель |
| | `lines(text)` | Разбить на строки через `|` |
| **Утилиты** | `length(s)` | Длина строки (число) |
| | `is_empty(s)` | `"true"` / `"false"` |
| | `is_numeric(s)` | `"true"` / `"false"` |
