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
python3 main.py;
```

- Docker
```bash
docker build -t poxstone/flask_any_response .;
# local
docker run --rm -it --net host -p 8080:8080 -p 5005:5005/udp poxstone/flask_any_response;
# production
docker run -itd --restart always --net host -e VERSION_DEP=MAIN -p 8080:8080 poxstone/flask_any_response;
```
- Publish
```bash
docker push poxstone/flask_any_response:latest;
```