FROM python:3.12.8-bookworm
LABEL authors="user"

# Установим рабочую директорию
WORKDIR /app

# Сначала скопируем только requirements.txt
COPY requirements.txt /app/requirements.txt

RUN \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Установим зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir  -r /app/requirements.txt

# Скопируем остальные файлы
COPY . /app

# Выполним миграции
RUN alembic upgrade head

EXPOSE 8000
# Укажем команду для запуска приложения
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]