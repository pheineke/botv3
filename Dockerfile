FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y git nano vim

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x start.sh

CMD ["./start.sh"]