# `json.hwk` — работа с JSON

Полноценная библиотека для чтения, записи и преобразования JSON.
Большинство операций являются built-ins. Запись в файл использует
Python backend из-за необходимости работы с файловой системой.

```
hawk

import json

set data = create_object("name:Hawk|version:1.0|active:true")
print pretty(data)

set nested = "{"
set nested = nested + "\"user\":"
set nested = nested + create_object("name:Mark|age:12")
set nested = nested + ",\"settings\":"
set nested = nested + create_object("theme:dark")
set nested = nested + "}"

print get(data, "name")
print get_nested(nested, "user.name")
print has_key(data, "token")
print keys(data)

set arr = create_array("10|20|30|hello")
print pretty(arr)
```

| **Категория** | **Функция** | **Описание** |
| --- | --- | --- |
| **Файлы** | `read_file(path)` | Читает JSON-файл, возвращает JSON-строку |
| | `write_file(path, json_str)` | Записывает JSON-строку в файл с отступами |
| **Парсинг** | `parse(json_str)` | Валидирует и переформатирует JSON |
| | `get(json_str, key)` | Значение по ключу (пусто, если нет) |
| | `get_nested(json_str, path)` | Вложенный ключ через `a.b.c` |
| | `has_key(json_str, key)` | `"true"` / `"false"` |
| | `keys(json_str)` | Ключи объекта через `|` |
| **Создание** | `stringify(value)` | Значение в JSON-строку |
| | `create_object(entries)` | Объект из `key:val` через `|` |
| | `create_array(items)` | Массив из элементов через `|` |
| | `set_key(json_str, key, value)` | Установить/создать ключ |
| | `delete_key(json_str, key)` | Удалить ключ |
| **Форматирование** | `pretty(json_str)` | Красивый вывод с отступами |
| | `minify(json_str)` | Упакованный вывод |

> **Примечание:** все значения из JSON возвращаются как строки.
> Для работы с числами используйте `to_number(json.get(data, "count"))`.
