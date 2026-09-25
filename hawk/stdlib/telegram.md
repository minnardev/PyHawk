# `telegram.hwk` — Telegram Bot API

Кроссплатформенный клиент для Telegram Bot API через HTTP. Не требует установки дополнительных библиотек.

```
hawk

import telegram

set token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
set bot = telegram_bot(token)

# Отправка сообщения
print send_message(bot, "me", "Hello from HAWK!")
print send_message(bot, "123456789", "Привет, пользователь!")

# Получение информации о боте
print get_me(bot)

# Получение обновлений
print get_updates(bot)
```

| **Функция** | **Что делает** |
| --- | --- |
| `telegram_bot(token)` | Создаёт объект бота из токена |
| `send_message(bot, chat_id, text)` | Отправляет текстовое сообщение, возвращает JSON |
| `get_me(bot)` | Возвращает информацию о боте |
| `get_updates(bot)` | Получает входящие обновления |
| `get_chat(bot, chat_id)` | Информация о чате |
| `edit_message(bot, chat_id, message_id, text)` | Редактирует сообщение |
| `delete_message(bot, chat_id, message_id)` | Удаляет сообщение |
| `answer_callback(bot, callback_query_id)` | Ответ на inline-запрос |
| `json_get_file(path, key)` | Извлекает поле из JSON-файла |
| `json_get_nested(path, field)` | Извлекает вложенное поле через точку, например `result.message_id` |

**Важно:**
- `send_message` возвращает полный JSON. Чтобы получить `message_id`, используй `json_get(resp, "message_id")`.
- `chat_id` — это число или строка: либо числовой ID, либо `@username`.
- Токен выдаёт [@BotFather](https://t.me/BotFather).
- Список методов: https://core.telegram.org/bots/api

**Пример: редактирование и удаление сообщения**

```hawk
import telegram
import os

set token = "123456:ABC-DEF"
set bot = telegram_bot(token)
set chat = 5050706507
set tmp = "/tmp/hawk_resp.json"

# Отправляем сообщение и сохраняем ответ во временный файл
set resp = send_message(bot, chat, "Первое сообщение")
file_write(tmp, resp)
set msg1 = json_get_nested(tmp, "result.message_id")

# Редактируем
set resp2 = edit_message(bot, chat, msg1, "Отредактировано!")
file_write(tmp, resp2)
set msg2 = json_get_nested(tmp, "result.message_id")

# Удаляем
delete_message(bot, chat, msg2)

# Или отправляем новое и удаляем через 2 секунды
set resp3 = send_message(bot, chat, "Временное сообщение")
file_write(tmp, resp3)
set msg3 = json_get_nested(tmp, "result.message_id")
sleep("2")
delete_message(bot, chat, msg3)

file_delete(tmp)
```
