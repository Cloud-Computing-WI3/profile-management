FROM python:3.10
ENV PYTHONBUFFERED 1

WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
COPY . .
CMD gunicorn --bind :8000 --workers 3 core.wsgi:application