FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/

EXPOSE 5556
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5556"]