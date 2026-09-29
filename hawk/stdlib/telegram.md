# `telegram.hwk` — Telegram Bot API

Обёртка над Telegram Bot API через built-in HTTP.
Без зависимостей от Python.

```
hawk

import telegram

set token = env("TELEGRAM_TOKEN")
set bot = telegram_bot(token)
set chat = 5050706507

set resp = send_message(bot, chat, "Hello from Hawk!")
print resp

set me = get_me(bot)
print me
```

| **Функция** | **Описание** |
| --- | --- |
| `telegram_bot(token)` | Сохранить токен |
| `send_message(bot, chat_id, text)` | Отправить сообщение |
| `get_me(bot)` | Информация о боте |
| `get_updates(bot)` | Получить обновления |
| `get_chat(bot, chat_id)` | Информация о чате |
| `edit_message(bot, chat_id, msg_id, text)` | Редактировать |
| `delete_message(bot, chat_id, msg_id)` | Удалить |
| `answer_callback(bot, query_id)` | Ответ на callback |

> Для безопасного хранения токена используй `env("TELEGRAM_TOKEN")`.
