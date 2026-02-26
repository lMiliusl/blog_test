# Создаем миграции для всех приложений
python manage.py makemigrations users
python manage.py makemigrations articles
python manage.py makemigrations comments

# Применяем миграции к базе данных
python manage.py migrate

# Запускаем сервер
python manage.py runserver
