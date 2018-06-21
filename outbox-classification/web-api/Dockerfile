FROM  python:3.6

WORKDIR /app

COPY requirements.txt /app
COPY server.py /app
COPY data /app/data
COPY public /app/public

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV REACT_APP_SERVICE_URL="http://localhost:5000"

EXPOSE 5000

ENTRYPOINT ["python", "server.py"]
