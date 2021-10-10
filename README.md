# Космический Телеграм

Телеграм бот, который получает фотографии от:
- [Astronomy Picture of the Day](https://apod.nasa.gov/apod/astropix.html)
- [DSCOVR's Earth Polychromatic Imaging Camera (EPIC)](https://epic.gsfc.nasa.gov/)
- [SpaceX REST API](https://github.com/r-spacex/SpaceX-API)

И публикует их раз в сутки в телеграм канале.

### Как установить

Для загрузки изображений от NASA необходим ключ к их API. Его можно получить [здесь](https://api.nasa.gov/).

Для запуска бота необходимо зарегeстрировать его, и создать канал в telegram. Инструкция [здесь](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/).

Полученные токены и ключи надо указать в файле `.env` и положить его в корень проекта. Для примера можно воспользоваться файлом `env_example`.   

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).