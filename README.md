# Blog API Project

Бэкенд для блога на Django + Django Ninja. Проект предоставляет API для управления пользователями, статьями, комментариями и категориями с аутентификацией по токену, логированием и полной контейнеризацией.

## Технологии
- Python 3.12, Django 4.2, Django Ninja
- PostgreSQL 15
- Docker, docker-compose
- pytest, GitHub Actions (CI/CD)

## Функциональные возможности
- Регистрация и аутентификация по токену (256 символов)
- CRUD для статей, категорий, комментариев (с проверкой прав)
- Админ-панель Django
- Логирование всех операций (ошибки, предупреждения, CRUD, вход/выход)
- Тестирование (22 теста, pytest)
- Контейнеризация и CI/CD

### Локальный запуск (без Docker)
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/username/blog.git
   cd blog

2. Создайте виртуальное окружение и установите зависимости:
    ```bash
    python -m venv venv
    source venv/bin/activate  # или venv\Scripts\activate на Windows
    pip install -r requirements.txt

3. Настройте базу данных (PostgreSQL) или используйте SQLite по умолчанию. Примените миграции:
    ```bash
    python manage.py migrate

4. Запустите сервер:
    ```bash
    python manage.py runserver

5. Откройте документацию API: http://localhost:8000/api/docs