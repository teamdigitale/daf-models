FROM  python:3.6

WORKDIR /app

ADD model.hdf5 /app
ADD requirements.txt /app
ADD server.py /app
ADD data /app/dataset
ADD public /app/public

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV REACT_APP_SERVICE_URL="http://localhost:5000"

EXPOSE 5000

ENTRYPOINT ["python", "server.py"]
