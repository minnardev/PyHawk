# `os.hwk` — работа с операционной системой

Кросс-платформенный интерфейс к ОС через built-ins.
Без зависимостей от Python.

```
hawk

import os

print current_os()      # macos / linux / windows
print is_macos()
print get_cwd()
print get_home()

set p = path_join("/home", "user/file.txt")
print path_dir(p)
print path_file(p)
print path_ext(p)

print file_exists("/tmp")
print dir_list("/tmp")
```

| **Категория** | **Функция** | **Описание** |
| --- | --- | --- |
| **Платформа** | `current_os()` | `macos`, `linux`, `windows` |
| | `is_macos()` | `"true"` / `"false"` |
| | `is_linux()` | `"true"` / `"false"` |
| | `is_windows()` | `"true"` / `"false"` |
| **Пути** | `path_join(a, b)` | Объединяет путь |
| | `path_dir(p)` | Директория файла |
| | `path_file(p)` | Имя файла |
| | `path_stem(p)` | Имя без расширения |
| | `path_ext(p)` | Расширение |
| | `path_abs(p)` | Абсолютный путь |
| | `path_norm(p)` | Нормализованный путь |
| **Файлы** | `file_read(path)` | Содержимое файла |
| | `file_write(path, content)` | Запись в файл |
| | `file_append(path, content)` | Дозапись |
| | `file_exists(path)` | `"true"` / `"false"` |
| | `file_is_file(path)` | `"true"` / `"false"` |
| | `file_is_dir(path)` | `"true"` / `"false"` |
| | `file_delete(path)` | `"true"` / `"false"` |
| | `file_copy(src, dst)` | Копирование |
| | `file_move(src, dst)` | Перемещение |
| | `file_size(path)` | Размер в байтах |
| **Директории** | `dir_create(path)` | Создать директорию |
| | `dir_delete(path)` | Удалить рекурсивно |
| | `dir_list(path)` | Список через `|` |
| | `dir_list_files(path)` | Только файлы |
| | `dir_list_dirs(path)` | Только директории |
| **Навигация** | `get_cwd()` | Текущая директория |
| | `get_home()` | Домашняя директория |
| | `chdir(path)` | Сменить директорию (built-in) |
| **Процессы** | `exec(cmd)` | Выполнить команду (built-in) |
| | `exec_bg(cmd)` | Фоновый запуск |
| | `sleep(seconds)` | Пауза |
| | `process_list()` | Список процессов |
| **Открытие** | `open_file(path)` | Открыть файл системным viewer |
| | `open_url(url)` | Открыть URL в браузере |
