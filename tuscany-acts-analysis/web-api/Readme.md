# Classification API

This project contains the api to classify outcome documents from Tuscany Region.

## how to develop

### Server

The server is a flask application.

1. create a virtual env

```
$ conda create --name ml-api python=3.6
$ source activate ml-api
```

2. run the server

```
$ python server.py
```

### Client

The client is done using [create-react-app](https://github.com/facebook/create-react-app). I'd suggest using [Node Version Manager]() to handle node dependency.
To run the app in dev mode

```
$ cd web-ui
$ npp start
```


## build a docker image

```bash

export ORGANIZATION=nexus.teamdigitale.test
export VERSION=0.0.7
docker build -t $ORGANIZATION/ml-api:$VERSION .
docker push $ORGANIZATION/ml-api:$VERSION
```

To run the docker images

```
docker run -dt --name mp-api -p 5000:5000 $ORGANIZATION/ml-api:$VERSION
```

```
curl -i -X POST \
  --url http://kong-admin.default.svc.cluster.local:8001/apis/ \
  --data 'name=ml-api' \
  --data 'uris=/ml-api' \
  --data 'upstream_url=http://ml-api-service.default.svc.cluster.local:5000'

```
