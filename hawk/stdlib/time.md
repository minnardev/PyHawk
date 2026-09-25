# `time.hwk` — дата и время

Все функции используют Python backend, поэтому форматирование стабильно на любой платформе.

```
hawk

import time

set t = now()
print "Сейчас:", t
print "Число:", timestamp()
print day_of_week()
print month(), year()
print clock()
```

| **Функция** | **Что возвращает** |
| --- | --- |
| `now()` | Дата и время: `YYYY-MM-DD HH:MM:SS` |
| `today()` | Дата: `YYYY-MM-DD` |
| `clock()` | Время: `HH:MM:SS` |
| `timestamp()` | Unix timestamp как число |
| `day_of_week()` | Название дня недели |
| `month()` | Название месяца |
| `year()` | Год |
| `hour()` | Часы |
| `minute()` | Минуты |
| `sleep_seconds(sec)` | Пауза на указанное количество секунд |
