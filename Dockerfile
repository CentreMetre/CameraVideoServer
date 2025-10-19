FROM python:3.10-slim-bookworm
LABEL authors="centremetre"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

COPY . .

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]