# requests.hwk — HTTP-запросы

Кроссплатформенный HTTP-клиент через Python backend.

```
hawk

import requests

set resp = get("https://httpbin.org/get")
print resp

set body = post("https://httpbin.org/post", "{\"key\": \"value\"}")
print body

set data = form_post("https://httpbin.org/post", {"key": "value"})
print data

set code = put("https://httpbin.org/put", "updated")
print code

set deleted = delete("https://httpbin.org/delete")
print deleted

set patch = patch("https://httpbin.org/patch", "patched")
print patch

set bin = download("https://httpbin.org/image/png", "image.png")
print file_exists(bin)
```

| **Метод** | **Что делает** |
| --- | --- |
| `get(url)` | GET-запрос, возвращает тело ответа |
| `post(url, json_str)` | POST с JSON-телом |
| `form_post(url, data)` | POST с form-data (dict как строка) |
| `put(url, data)` | PUT-запрос |
| `delete(url)` | DELETE-запрос |
| `patch(url, data)` | PATCH-запрос |
| `download(url, path)` | Скачивает файл, возвращает путь |
| `status_code(resp)` | Извлекает код ответа из строки |

**Примечание:** Все данные передаются как строки. Для JSON используй `post()` или `json_encode()`. Файлы скачиваются через `download()`.
