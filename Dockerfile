FROM python:3.11-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /cnvte_webpage
COPY  requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PORT 8080

# CMD python manage.py runserver 0.0.0.0:8080

#FROM apache/airflow:2.8.1
# USER airflow

# RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" kafka-python
# COPY requirements.txt /requirements.txt
# RUN pip install --user --upgrade pip
# RUN pip install --no-cache-dir --user -r /requirements.txt