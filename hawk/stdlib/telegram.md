# `telegram.hwk` — Telegram Bot API

Полноценная библиотека для создания Telegram-ботов на языке Hawk.
Работает через встроенные функции HTTP и JSON без внешних зависимостей.

```hawk
import telegram

# 1. Инициализируем бота
set token = env("TELEGRAM_BOT_TOKEN")
set bot = telegram_bot(token)

# 2. Получаем информацию о боте
print get_me(bot)

# 3. Отправляем сообщение
send_message(bot, 123456789, "Привет из Hawk!")
```

---

## 📋 Таблица функций

### 💬 Сообщения и переписка
| Функция | Описание |
| --- | --- |
| `send_message(bot, chat_id, text)` | Отправить обычное текстовое сообщение |
| `send_message_html(bot, chat_id, html_text)` | Отправить сообщение с HTML-разметкой (`<b>жирный</b>`, `<i>курсив</i>`, `<code>код</code>`) |
| `send_message_markdown(bot, chat_id, md_text)` | Отправить сообщение с MarkdownV2-разметкой |
| `reply_to(bot, chat_id, message_id, text)` | Ответить реплаем на конкретное сообщение |
| `edit_message(bot, chat_id, message_id, text)` | Отредактировать текст отправленного сообщения |
| `delete_message(bot, chat_id, message_id)` | Удалить сообщение по его ID |
| `pin_message(bot, chat_id, message_id)` | Закрепить сообщение в чате |
| `unpin_message(bot, chat_id, message_id)` | Открепить сообщение |

### 📷 Медиа и файлы
| Функция | Описание |
| --- | --- |
| `send_photo(bot, chat_id, photo_url, caption)` | Отправить фото по ссылке (URL) с подписью |
| `send_document(bot, chat_id, doc_url, caption)` | Отправить файл/документ по прямой ссылке |
| `send_voice(bot, chat_id, voice_url, caption)` | Отправить голосовое сообщение |
| `send_sticker(bot, chat_id, sticker_id)` | Отправить стикер по его `file_id` |
| `send_location(bot, chat_id, latitude, longitude)` | Отправить геолокацию на карте |

### ⚡ Действия и статус (UX)
| Функция | Описание |
| --- | --- |
| `send_action(bot, chat_id, action)` | Показать статус действия бота: `"typing"` (печатает...), `"upload_photo"` (загружает фото...), `"record_voice"`, `"upload_document"` |

### ℹ️ Информация
| Функция | Описание |
| --- | --- |
| `get_me(bot)` | Информация о самом боте (`username`, `id`, имя) |
| `get_chat(bot, chat_id)` | Информация о чате/пользователе |

### 🔄 Поллинг и Callback'и
| Функция | Описание |
| --- | --- |
| `get_updates(bot)` | Получить свежие входящие сообщения и события (JSON) |
| `get_updates_offset(bot, offset)` | Запросить новые события с оффсетом (для long-polling) |
| `answer_callback(bot, query_id)` | Подтвердить нажатие инлайн-кнопки |
| `answer_callback_alert(bot, query_id, text)` | Показать всплывающее окно-алерт по кнопке |

### 🔍 Хелперы извлечения данных (Extractors)
Позволяют моментально достать данные последнего сообщения без ручного парсинга длинного JSON:
| Функция | Описание |
| --- | --- |
| `extract_last_update_id(updates)` | ID последнего апдейта (нужен для смещения оффсета) |
| `extract_last_chat_id(updates)` | ID чата отправителя последнего сообщения |
| `extract_last_text(updates)` | Текст последнего сообщения |
| `extract_last_username(updates)` | Username отправителя |
| `extract_last_message_id(updates)` | ID последнего сообщения |

---

## 🚀 Примеры использования

### Пример 1: Отправка красивого сообщения с HTML и фото
```hawk
import telegram

set token = "123456789:ABCdefGhIJKlmNoPQRstuVWxYZ"
set bot = telegram_bot(token)
set chat_id = 987654321

# Показываем статус "печатает..."
send_action(bot, chat_id, "typing")

# Отправляем форматированное сообщение
send_message_html(bot, chat_id, "🦅 <b>Привет из PyHawk!</b>\nКод работает <i>нативно</i> без внешних либ.")

# Отправляем картинку
send_photo(bot, chat_id, "https://picsum.photos/400/300", "Случайная картинка дня!")
```

---

### Пример 2: Полноценный Эхо-Бот на Hawk (Long-Polling)
```hawk
import telegram
import color

set token = env("TELEGRAM_BOT_TOKEN")
if (token = "") {
    print red("Укажите переменную окружения TELEGRAM_BOT_TOKEN!")
}

set bot = telegram_bot(token)
print green("Бот запущен и слушает сообщения...")

set last_offset = 0

set running = true
while (running = true) {
    # Запрашиваем новые сообщения
    set updates = get_updates_offset(bot, last_offset)
    set upd_id = extract_last_update_id(updates)

    if (upd_id != "" and to_number(upd_id) >= last_offset) {
        set chat_id = extract_last_chat_id(updates)
        set text = extract_last_text(updates)
        set user = extract_last_username(updates)

        print "Новое сообщение от @" + user + ": " + text

        # Отвечаем пользователю
        if (text = "/start") {
            send_message(bot, chat_id, "Привет, " + user + "! Я бот, написанный на языке Hawk 🦅")
        } else {
            send_message(bot, chat_id, "Эхо: " + text)
        }

        # Сдвигаем оффсет, чтобы не обрабатывать повторно
        set last_offset = to_number(upd_id) + 1
    }
}
```
