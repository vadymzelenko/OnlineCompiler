FROM python:3.11-slim

WORKDIR /app

# Docker CLI: the Celery worker launches isolated sandbox containers.
RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
