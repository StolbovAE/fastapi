FROM python:3.11

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 5002