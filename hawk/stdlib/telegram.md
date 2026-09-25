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
| `send_message(bot, chat_id, text)` | Отправляет текстовое сообщение |
| `get_me(bot)` | Возвращает информацию о боте |
| `get_updates(bot)` | Получает входящие обновления |
| `get_chat(bot, chat_id)` | Информация о чате |
| `edit_message(bot, chat_id, message_id, text)` | Редактирует сообщение |
| `delete_message(bot, chat_id, message_id)` | Удаляет сообщение |
| `answer_callback(bot, callback_query_id)` | Ответ на inline-запрос |

**Важно:**
- Все функции возвращают JSON как строку. Используй `json_decode()` для парсинга.
- `chat_id` — это строка: либо числовой ID, либо `@username`.
- Токен выдаёт [@BotFather](https://t.me/BotFather).
- Список методов: https://core.telegram.org/bots/api
