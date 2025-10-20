FROM python:3.10-slim-bookworm
LABEL authors="centremetre"

WORKDIR /app

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

ENV IMGDB=imgdata.db
ENV RECDB=recdata.db
ENV DBSUFFIX=data.db

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

COPY . .

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]