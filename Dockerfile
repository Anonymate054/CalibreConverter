FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y calibre

WORKDIR /app

COPY . ./

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD exec uvicorn main:app --host 0.0.0.0 --port 8080