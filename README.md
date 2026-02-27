# Создаем миграции для всех приложений
python manage.py makemigrations users <br/>
python manage.py makemigrations articles <br/>
python manage.py makemigrations comments <br/>

# Применяем миграции к базе данных
python manage.py migrate <br/>

# Запускаем сервер
python manage.py runserver <br/>
