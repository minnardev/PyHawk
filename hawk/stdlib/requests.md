# `requests.hwk` — HTTP-запросы

Кросс-платформенные HTTP-запросы через built-ins.
Без зависимостей от Python.

```
hawk

import requests

set resp = get("https://httpbin.org/get")
print status_code(resp)

set post_resp = post("https://httpbin.org/post", "{\"a\":1}")
print post_resp

download("https://example.com/file.txt", "/tmp/file.txt")
```

| **Функция** | **Описание** |
| --- | --- |
| `get(url)` | GET-запрос |
| `post(url, data)` | POST с телом |
| `put(url, data)` | PUT с телом |
| `delete(url)` | DELETE |
| `patch(url, data)` | PATCH с телом |
| `download(url, path)` | Скачать файл |
| `status_code(resp_text)` | Извлечь HTTP код |
