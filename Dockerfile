FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev python3-pip python3-venv wget libxcb-cursor0 libegl1 libopengl0

RUN wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sh /dev/stdin

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8080

CMD exec uvicorn app.main:app --host 0.0.0.0 --port 8080