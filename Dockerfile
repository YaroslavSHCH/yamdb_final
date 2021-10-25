FROM python:3.8.5

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
CMD gunicorn manage.py runserver 0:8000
COPY . /code