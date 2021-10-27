### YaMDB app ![YaMDB app](https://github.com/YaroslavSHCH/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
### Описание
Учебный проект для Я.Практикума
### Технологии
Python 3.7 , Django 2.2.6
- Docker 3.8
- Nginx
- Gunicorn
- Pytest

### Запуск проекта

- Запускаем сборку контейнеров командой:
```
docker-compose up --build 
```
с флагом ```-d``` запуск произойдет в фоновом режиме.

Спустя некотрое время контейнер запустится и появится сообщение о запуске контейнеров:
```
Starting yamdb_db_1 ... done
Starting yamdb_web_1 ... done
Starting yamdb_nginx_1 ... done
```

### Проверка работоспобности
- Проводим миграции.
- Если нет статики выполняем:
```
docker-compose exec web python manage.py collectstatic
````
- Создаем суперпользователя для работы с админкой. Указываем емейл, логин и пароль
``` 
docker-compose exec web python manage.py createsuperuser

Email: practikum@yandex.ru
Username: practikum
Password: 
Password (again): 

Superuser created successfully.


```

# Админка
- Открываем админку <http://84.201.154.67/admin>:
![django-form-auth](git_image/django_login.png)

- Вводим данные суперпользователя и авторизуемся:
![django-log-in](git_image/django_admin.png)

```Done!```

### Автор
Ярослав
