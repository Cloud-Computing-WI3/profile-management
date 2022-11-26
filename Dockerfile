FROM python:3.10
ENV PYTHONBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runservere 0.0.0.0:80