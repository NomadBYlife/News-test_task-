# Test task

## About
In this project, tasks were implemented according to the technical specifications


### Stack used

Python<br>
Django<br>
DRF<br>
JWT authenticated<br>
Celery<br>
Docker

## Quick Start

Quick guide for MacOs/Linux:
<br>

If you are using SSH: `git clone git@github.com:NomadBYlife/News-test_task-.git`

If https: `git clone https://github.com/NomadBYlife/News-test_task-.git`


Enter next command:


`python3 -m venv venv` <br>
`source venv/bin/activate`<br>
`pip install -r requirements.txt`<br>
`python manage.py makemigrations`<br>
`python manage.py migrate`<br>
<br>
Create superuser(admin):<br>
`python manage.py createsuperuser`<br>
<br>
Username: `admin`<br>
Email: if you want, not necessary<br>
Password: `admin`<br>
Confirm password: `admin`<br>
<br>
Go to the admin part and fill in the "Rating Score". For example 1,2,3<br>
Starting with docker-compose: 
1. Go to /application/settings uncomment the parameter "REDIS_HOST='redis'"
2. Enter command in terminal `docker-compose up --build`

Staring with terminal: <br>
1. Go to /application/settings uncomment the parameter "REDIS_HOST='0.0.0.0'"
2. Enter command in terminal `python manage.py runserver`<br>



API endpoints: <br>
http://127.0.0.1:8000/api/v1/news/  - all articles <br>
http://127.0.0.1:8000/api/v1/news/vendorecode(id)   -  getting a specific article (takes VendorCode(Id) as a parameter) <br>
JWT authentication <br>
http://127.0.0.1:8000/api/v1/token/      <br>
http://127.0.0.1:8000/api/v1/token/refresh/     <br>
http://127.0.0.1:8000/api/v1/token/verify/      <br>
Only for authenticated users
http://127.0.0.1:8000/api/v1/news/my_news/   -   getting all user articles <br>
http://127.0.0.1:8000/api/v1/news/my_news/vendorecode(id)   -  update/delete a specific user article <br>
http://127.0.0.1:8000/api/v1/news/my_news/favorites/   -   list of user's favorite articles<br>
http://127.0.0.1:8000/api/v1/news/my_news/create/   -   create a new article<br>
