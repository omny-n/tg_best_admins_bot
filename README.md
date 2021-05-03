# Telegram admins chatbot

## Описание

Бот написан на [aiogram](https://github.com/aiogram/aiogram) с использованием [sqlite](https://sqlite.org/index.html).

Бот для удобного администрирования чата админов телеграм-каналов. Бот хранит в базе информацию об админах чата и их телеграм-каналах. Доступны следующие команды:

* `/add @channel ID_категории описание до 50 символов` – добавит канал и иформацию об администраторе канала в базу, доступные категории и их айди можно посмотреть в `/help`. Добавлять можно только свои каналы, так как бот хранит информацию о пользователе по телеграм-ID. 
* `/channel` – ответив этой командой на любое сообщение, можно увидеть каналы пользователя из реплая. Если использовать команду без реплая, бот покажит ваши каналы.
* `/my_channels` – посомтреть свой списко каналаов.
* `/list` – список всех всех админов и их каналов по категориям.
* `/search нвазание канала` – поиск по нвазванию.
* `/del ID_канала` – удаление канала из базы по ID. 



## Установка

Для сборки docker-контейнера:
```docker
docker build -t tg_bot ./
```

Команда для запуска: 
```docker
docker run -d --restart=always --name bot -v /bot_db_volume:/home/db -e TELEGRAM_API_TOKEN="" -e ACCESS_ID="" tg_bot
``` 

`bot_db_volume` – docker volume

`TELEGRAM_API_TOKEN=""` – токен бота

`ACCESS_ID=""` – айди чата в котором используется бот.
