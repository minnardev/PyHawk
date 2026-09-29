# `json.hwk` — работа с JSON

Полноценная библиотека для чтения, записи и преобразования JSON.
Все парсинг и сериализация выполняются через Python backend,
поэтому работает одинаково на macOS, Linux и Windows.

```
hawk

import json

# Чтение из файла
set data = json.read_file("config.json")

# Получение значений
print json.get(data, "name")
print json.get_nested(data, "user.profile.age")

# Проверка ключа
if (json.has_key(data, "token") = "true") {
    print "Token exists"
}

# Построение JSON
set obj = json.create_object("name:Hawk|version:1.0")
set arr = json.create_array("1|2|3|hello")

# Форматирование
print json.pretty(obj)
print json.minify(obj)
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
