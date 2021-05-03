FROM python:3.9

WORKDIR /home

RUN pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3

COPY *.py ./
COPY createdb.sql ./

ENTRYPOINT ["python", "bot.py"]