FROM python:3.10
ENV PYTHONBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt
CMD python manage.py runserver 0.0.0.0:80