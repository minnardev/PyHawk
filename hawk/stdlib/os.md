# `os.hwk` — файловая система и процессы

Функции возвращают строки, числа или `true`/`false`, поэтому их можно **вкладывать** в условия и конкатенацию:

```
hawk

import "os"

set home = get_home()
set docs = path_join(home, "Documents")
set log  = path_join(docs, "app.log")

if (not file_exists(log)) {
    file_write(log, "Hello Hawk!")
}

print file_read(log)
print "Size:", file_size(log), "bytes"

dir_create(path_join(docs, "projects"))
print dir_list(docs)
```

| **Функция** | **Что делает** |
| --- | --- |
| `current_os()` | Возвращает `"macos"`, `"linux"` или `"windows"` |
| `is_macos()` / `is_linux()` / `is_windows()` | Проверка платформы |
| `path_join(a, b)` | Соединяет два пути |
| `path_dir(p)` | Каталог из пути |
| `path_file(p)` | Имя файла с расширением |
| `path_stem(p)` | Имя файла без расширения |
| `path_ext(p)` | Расширение файла |
| `path_abs(p)` | Абсолютный путь |
| `path_norm(p)` | Нормализованный путь (без `.` и `..`) |
| `file_exists(path)` | Существует ли файл или каталог |
| `file_is_file(path)` | Это именно файл |
| `file_is_dir(path)` | Это именно каталог |
| `file_read(path)` | Читает файл и возвращает строку |
| `file_read_lines(path)` | То же, что `file_read` |
| `file_write(path, text)` | Записывает строку в файл |
| `file_append(path, text)` | Дописывает строку в конец файла |
| `file_delete(path)` | Удаляет файл |
| `file_copy(src, dst)` | Копирует файл |
| `file_move(src, dst)` | Перемещает файл |
| `file_size(path)` | Размер файла в байтах |
| `dir_exists(path)` | Существует ли каталог |
| `dir_create(path)` | Создаёт каталог (включая родительские, как `mkdir -p`) |
| `dir_create_recursive(path)` | Синоним `dir_create` |
| `dir_delete(path)` | Удаляет каталог рекурсивно |
| `dir_list(path)` | Списокentries в каталоге (по одной строке) |
| `dir_list_files(path)` | Только файлы в каталоге |
| `dir_list_dirs(path)` | Только подкаталоги |
| `get_cwd()` | Текущий рабочий каталог |
| `chdir(path)` | Переходит в каталог (встроенная функция, доступна глобально) |
| `get_home()` | Домашний каталог |
| `exec(cmd)` | Выполняет команду в shell |
| `exec_bg(cmd)` | Выполняет команду в фоне |
| `sleep(seconds)` | Пауза |
| `kill_pid(pid)` | Убивает процесс |
| `process_list()` | Список процессов |
| `open_file(path)` | Открывает файл системным viewer |
| `open_url(url)` | Открывает URL в браузере |
