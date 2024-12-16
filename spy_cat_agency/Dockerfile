# Використовуємо офіційний образ Python
FROM python:3.11-slim

# Встановлюємо залежності для системи
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl postgresql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Встановлюємо Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Додаємо шлях для Poetry до змінних середовища
ENV PATH="/root/.local/bin:$PATH"

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файли проекту в контейнер
COPY pyproject.toml poetry.lock /app/

# Встановлюємо залежності через Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копіюємо весь проект
COPY . /app

# Відкриваємо порт для доступу до веб-сервера
EXPOSE 8000

# Запускаємо сервер
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
