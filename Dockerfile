FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание пользователя
RUN useradd --create-home --shell /bin/bash app
USER app

EXPOSE 8000

# По умолчанию запускаем сервис ауфа
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
