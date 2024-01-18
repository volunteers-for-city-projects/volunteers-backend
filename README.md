# backend for volunteers for city projects
REST API для Проекта Платформа для волонтеров

![example workflow](https://github.com/volunteers-for-city-projects/volunteers-backend/actions/workflows/main.yml/badge.svg)

[http://better-together.acceleratorpracticum.ru/](https://2260993-dk30711.twc1.net/) 

Админ панель доступна по ссылке [http://better-together.acceleratorpracticum.ru/admin/](https://2260993-dk30711.twc1.net/admin)  
### (в процессе разработки, может надо api)
Документация доступна по ссылке [http://better-together.acceleratorpracticum.ru/swagger/](https://2260993-dk30711.twc1.net/admin/swagger/)

## Стек технологий:

* [Python 3.10.6](https://www.python.org/downloads/)
* [Django 4.2.6](https://www.djangoproject.com/download/)
* [Django Rest Framework 3.14](https://pypi.org/project/djangorestframework/#files)

## Как запустить проект локально (необходим установленный Python3.10.6):

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:volunteers-for-city-projects/volunteers-backend.git
```

```
cd volunteers-backend/
```


Cоздать виртуальное окружение:

```
python3 -m venv venv
```

Активировать созданное виртуальное окружение:

- для Linux
```
source venv/bin/activate
```

- для Windows
```
venv\Scripts\activate.bat
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r ./backend/requirements.txt
```

Перемещаемся в директорию backend для дальнейшей работы:

```
cd backend/
```

Выполнить миграции:


для корректной работы следующих команд необходим файл .env
в директории infra_bt, созданный по шаблону файла .env.example в той же
директории и подготовлена БД postgresql с соответствующими настройками.

```
python3 manage.py migrate
```

Создание суперпользователя (если необходим доступ в админку Django):


При создании будет затребовано ввести "Роль:" - вводим admin:
```
python3 manage.py createsuperuser
```

Запустить проект:

```
python3 manage.py runserver
```


### Документация для Проекта станет доступна по адресу:

http://localhost:8000/swagger/



### Админка станет доступна по адресу:

http://localhost:8000/admin/


## Как запустить проект локально в Docker контейнерах (необходим установленный docker + docker-compose или Docker Desktop):

Клонировать репозиторий и перейти в директорию infra_bt проекта:

```
git clone git@github.com:volunteers-for-city-projects/volunteers-backend.git
```

```
cd volunteers-backend/infra_bt/
```

Подготовить .env файл по шаблону файла .env.example

Запустить сборку Docker контейнеров проекта:
```
docker compose up -d
```


### Документация для Проекта станет доступна по адресу:

http://localhost:8000/swagger/



### Админка станет доступна по адресу:

http://localhost:8000/admin/
