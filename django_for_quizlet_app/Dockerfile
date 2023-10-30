# Используем базовый образ Python
FROM python:latest

# Устанавливаем переменные среды
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и код в контейнер
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app/

# Запускаем команду для запуска Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]