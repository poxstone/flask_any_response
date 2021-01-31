# Simple response all url

## Local excecution

- Install
```bash
python3 -m virtualenv venv;
source venv/bin/activate;
python3 -m pip install -r requirements.txt;
```
- Run
```bash
python3 application.py;
```

- Docker
```bash
docker build -t poxstone/flask_any_response .;
# local
docker run --rm -it --net host -p 8080:8080 -p 5005:5005/udp poxstone/flask_any_response;
# production
docker run -itd --restart always --net host -e VERSION_DEP=MAIN -p 8080:8080 -p 5005:5005/udp poxstone/flask_any_response;
```
- Publish
```bash
docker push poxstone/flask_any_response:latest;
```


# test
> ***GET parameters***:
> - path: use for send aditional path ex: "?path=/administrative/portal"
> - method: use for change method ex: "?method=POST"

```bash
# levels
curl -X GET "http://localhost:8080/lv1/lv2";
curl -X POST "http://localhost:8080/lv1/lv2";

# udp send
curl -X GET "http://localhost:8080/testudp/?UDP_IP=127.0.0.1&UDP_PORT=5006&MESSAGE=hola";

# proxy sender
curl -X GET "http://localhost:8080/requests/https/eltiempo.com/443/?path=/opinion/columnistas/martha-senn&other=none";
# POST 1
curl -X POST "http://localhost:8080/requests/https/jsonplaceholder.typicode.com/443/?path=/posts" -H "Content-Type: application/json" -d '{"hola":"perro"}';
# POST 2 (parameter method=POST)
curl -X GET "http://localhost:8080/requests/https/jsonplaceholder.typicode.com/443/?path=/posts&method=POST";

# command
curl -X POST "http://localhost:8080/do/com/" -H "Content-Type: application/json" -d '{"command":["ping","-c","2","8.8.8.8"]}';


```