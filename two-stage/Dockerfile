FROM python:3.10-slim

WORKDIR /app

# Install system dependencies first (libgomp1 is required for implicit)
RUN apt-get update && apt-get install -y libgomp1

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/

EXPOSE 5555
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555"]