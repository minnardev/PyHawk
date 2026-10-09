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

set auth_resp = post_headers("https://api.example.com", "{\"query\":\"test\"}", "{\"Authorization\": \"Bearer token\"}")
print auth_resp

download("https://example.com/file.txt", "/tmp/file.txt")
```

| **Функция** | **Описание** |
| --- | --- |
| `get(url)` | GET-запрос |
| `post(url, data)` | POST с телом |
| `post_headers(url, data, headers_json)` | POST с телом и кастомными HTTP-заголовками (JSON) |
| `put(url, data)` | PUT с телом |
| `delete(url)` | DELETE |
| `patch(url, data)` | PATCH с телом |
| `download(url, path)` | Скачать файл |
| `status_code(resp_text)` | Извлечь HTTP код |
