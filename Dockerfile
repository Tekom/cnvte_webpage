FROM python:3.11-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /cnvte_webpage
COPY  requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PORT 8080
CMD python manage.py runserver 0.0.0.0:8080