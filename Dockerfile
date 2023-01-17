FROM python:3.10
ENV PYTHONBUFFERED 1

WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p static
RUN python manage.py collectstatic --noinput
CMD gunicorn --bind :80 --workers 1 core.wsgi:application