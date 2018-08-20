FROM  python:3.6

WORKDIR /app

COPY outbox-classification/web-api/requirements.txt /app
COPY outbox-classification/web-api/server.py /app
COPY outbox-classification/web-api/data /app/data
COPY outbox-classification/web-api/public /app/public

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV REACT_APP_SERVICE_URL="http://localhost:5000"

EXPOSE 5000

ENTRYPOINT ["python", "server.py"]
