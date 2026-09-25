# `color.hwk` — цвета и стили текста в терминале

Использует ANSI escape-коды. Работает в macOS Terminal, iTerm2, Linux и Windows Terminal.

```
hawk

import color

print red("Ошибка!")
print green("Успешно")
print bold(blue("Заголовок"))
print yellow("Предупреждение: " + blink("Внимание!"))
```

| **Функция** | **Цвет / стиль** |
| --- | --- |
| `red(text)` | Красный |
| `green(text)` | Зелёный |
| `yellow(text)` | Жёлтый |
| `blue(text)` | Синий |
| `magenta(text)` | Пурпурный |
| `cyan(text)` | Бирюзовый |
| `white(text)` | Белый |
| `gray(text)` | Серый |
| `bold(text)` | Жирный |
| `dim(text)` | Приглушённый |
| `italic(text)` | Курсив |
| `underline(text)` | Подчёркивание |
| `blink(text)` | Мигание |
| `strikethrough(text)` | Зачёркивание |
| `bg_red(text)` | Красный фон |
| `bg_green(text)` | Зелёный фон |
| `bg_yellow(text)` | Жёлтый фон |
| `bg_blue(text)` | Синий фон |
| `bg_magenta(text)` | Пурпурный фон |
| `bg_cyan(text)` | Бирюзовый фон |
| `reset()` | Сброс всех атрибутов |
| `clear()` | Очищает экран терминала |
