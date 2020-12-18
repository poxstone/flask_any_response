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
```bash
# levels
curl -X GET "http://localhost:8080/lv1/lv2";
curl -X POST "http://localhost:8080/lv1/lv2";

# udp send
curl -X GET "http://localhost:8080/testudp/?UDP_IP=127.0.0.1&UDP_PORT=5006&MESSAGE=hola";
```