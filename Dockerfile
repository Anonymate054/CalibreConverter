FROM python:3.12-slim

WORKDIR /app

COPY . /app/

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev python3-pip python3-venv wget libxcb-cursor0 libegl1 libopengl0

RUN wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sh /dev/stdin

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PORT 8080

EXPOSE 8080

CMD exec uvicorn app.main:app --host 0.0.0.0 --port 8080