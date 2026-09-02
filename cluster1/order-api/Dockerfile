FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask pymongo

COPY app.py /app/app.py

EXPOSE 3000

CMD ["python", "/app/app.py"]
