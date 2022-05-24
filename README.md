# Тестовое задание

## О проекте
В этом проекте были реализованы задания по ТЗ


### Используемый стек

Python<br>
Django<br>
DRF<br>
JWT authenticated<br>
Celery<br>
Docker

## Быстрый старт

Краткое руководство для MacOs/Linux:

Откройте терминал и перейдите в директорию где будет лежать ваш проект. <br>
Если вы используете SSH введите команду : `git@github.com:NomadBYlife/News-test_task-.git`

Если вы используете https: `https://github.com/NomadBYlife/News-test_task-.git`


Далее команды:


`python3 -m venv venv` <br>
`source venv/bin/activate`<br>
`cd News`<br>
`pip install -r requirements.txt`<br>
`python manage.py migrate`<br>
<br>
Создайте суперпользователя (администратора):<br>
`python manage.py createsuperuser`<br>
<br>
Username: `admin`<br>
Email: по желанию, не обязательно <br>
Password: `admin`<br>
Confirm password: `admin`<br>
<br>

Запуск через docker-compose: 
1. Зайдите в News/application/settings раскомментируйте параметр "REDIS_HOST='redis'"
2. Введите команду в терминале `docker-compose up --build`

Запуск через терминал: <br>
1. Зайдите в News/application/settings раскомментируйте параметр "REDIS_HOST='0.0.0.0'"
2. `python manage.py runserver`<br>



API endpoints: <br>
http://127.0.0.1:8000/api/v1/news/  - получение всех статей <br>
http://127.0.0.1:8000/api/v1/news/vendorecode(id)   -  получение конкретной статьи(принимает ВендорКод, он же Id, как параметр) <br>
JWT аутентификация <br>
http://127.0.0.1:8000/api/v1/token/      <br>
http://127.0.0.1:8000/api/v1/token/refresh/     <br>
http://127.0.0.1:8000/api/v1/token/verify/      <br>
Только для аутентифицированных пользователей
http://127.0.0.1:8000/api/v1/news/my_news/   -   получение всех пользовательских авторских статей <br>
http://127.0.0.1:8000/api/v1/news/my_news/vendorecode(id)   -  изменение/удаление конкретной пользовательской статьи <br>
http://127.0.0.1:8000/api/v1/news/my_news/favorites/   -   список избранных статей пользователя<br>
http://127.0.0.1:8000/api/v1/news/my_news/create/   -   создание новой статьи<br>