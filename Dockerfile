FROM python:3.12-slim


RUN mkdir /app


WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1


RUN pip install --upgrade pip


COPY requirements.txt /app


RUN pip install -r requirements.txt

COPY . /app
ENV PYTHONPATH="${PYTHONPATH}:/app"
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "zampa.wsgi:application"]