FROM python:3.8-slim

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get clean

WORKDIR /app
COPY requirements.txt requirements.txt

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "server.py"]
