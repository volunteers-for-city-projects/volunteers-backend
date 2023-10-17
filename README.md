# backend for volunteers for city projects
REST API для Проекта Платформа для волонтеров

![example workflow](https://github.com/volunteers-for-city-projects/volunteers-backend/actions/workflows/main.yml/badge.svg)

[http://better-together.acceleratorpracticum.ru/](http://better-together.acceleratorpracticum.ru/)

Админ панель доступна по ссылке [http://better-together.acceleratorpracticum.ru/admin/](http://better-together.acceleratorpracticum.ru/admin/)
### (в процессе разработки, может надо api)
Документация доступна по ссылке [http://better-together.acceleratorpracticum.ru/swagger/](http://better-together.acceleratorpracticum.ru/swagger/)

## Стек технологий:

* [Python 3.10.6](https://www.python.org/downloads/)
* [Django 4.2.6](https://www.djangoproject.com/download/)
* [Django Rest Framework 3.14](https://pypi.org/project/djangorestframework/#files)

### Как запустить проект локально:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:volunteers-for-city-projects/backend.git
```

```
cd backend
```


Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```


## Документация для Проекта доступна по адресу:

```http://127.0.0.1:8000/swagger/```



## Админка (в разработке)

http://localhost:8000/admin/

Логин admin@admin.com
Пароль admin

