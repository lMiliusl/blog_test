# Blog API

Бэкенд для блога с использованием Django и Django Ninja. Реализована регистрация пользователей, создание статей и комментариев, админ-панель, логирование и тестирование. Проект полностью контейнеризирован с помощью Docker и поддерживает CI/CD через GitHub Actions.

## Технологии

- Python 3.12
- Django 4.2
- Django Ninja (для API)
- PostgreSQL 15
- Docker & Docker Compose
- pytest (тестирование)
- GitHub Actions (CI/CD)

## Функциональность

- Регистрация и аутентификация пользователей по токену (256 символов)
- CRUD для статей (только автор может редактировать/удалять)
- CRUD для комментариев (с поддержкой вложенных ответов)
- Админ-панель для управления пользователями, статьями, категориями и комментариями
- Логирование действий (вход/выход, CRUD-операции, ошибки)
- Docker-контейнеризация (Django + PostgreSQL)
- Автоматическое тестирование и деплой через GitHub Actions

## Установка и запуск

### Локально (без Docker)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/username/blog_test.git
   cd blog_test

2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt

4. Настройте базу данных (по умолчанию используется SQLite). Для PostgreSQL укажите переменные окружения:
   ```bash
   export DB_NAME=blog_db
   export DB_USER=blog_user
   export DB_PASSWORD=P@ssw0rd
   export DB_HOST=localhost
   export DB_PORT=5432

5. Выполните миграции:
    ```bash
    python manage.py makemigrations
    python manage.py migrate

6. Запустите сервер разработки:
   ```bash
   python manage.py runserver

### Запуск через Docker

1. Убедитесь, что Docker и Docker Compose установлены.

2. В корне проекта выполните:
   ```bash
   docker-compose up --build

3. Приложение будет доступно по адресу:
   - API: http://localhost:8000/api
   - Админка: http://localhost:8000/admin

## Использование API

### Аутентификация

- Регистрация - POST /api/users/register с JSON {"username": "...", "password": "..."}
- Логин - POST /api/users/login (с теми же полями)
- Все защищённые эндпоинты требуют заголовок - Authorization: Bearer <token>

### Основные эндпоинты

- Статьи - GET /api/articles/, POST /api/articles/, GET /api/articles/{id}, PUT /api/articles/{id}, DELETE /api/articles/{id}
- Категории - GET /api/articles/categories, POST /api/articles/categories (только для авторизованных)
- Комментарии -  GET /api/articles/{article_id}/comments, POST /api/comments, PUT /api/comments/{id}, DELETE /api/comments/{id}

Подробная документация OpenAPI доступна по адресу:  http://localhost:8000/api/docs

## Тестирование

Проект использует  pytest для тестирования. Запуск тестов:

    pytest

Или с отчётом о покрытии:

    pytest --cov=apps

## CI/CD

Настроен пайплайн GitHub Actions, который:
1. Запускает тесты на каждый push и pull request.
2. При пуше в ветки  main или  master собирает Docker-образ и публикует его в Docker Hub.
3. Автоматически деплоит новую версию на VPS (через SSH).

Для работы CI/CD необходимо добавить секреты в репозиторий:
-  DOCKER_USERNAME / DOCKER_PASSWORD
-  VPS_HOST / VPS_USER / VPS_SSH_KEY
