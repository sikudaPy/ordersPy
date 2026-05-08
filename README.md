Небольшой аналог составления заказов в Интеренете по мотивам 1C Devcon2024 
https://developer.1c.ru/applications/Console?state=931c01dad1

Попытка реализации на Python Django
Установка:
1. Сделать окружение и активизировать его
python -m venv venv
2. Активизируйте его
venv/Scripts/activate (source venv/bin/activate)
3.  Установка пакетов
pip install -r requirements.txt
4. Сделать миграцию
python manage.py makemigrations orders feedback
python manage.py migrate
5. Сделать админа
python manage.py createsuperuser
6. Запустить python manage.py runserver
7. В Админке настроить НСИ - http://127.0.0.1:8000/admin/
