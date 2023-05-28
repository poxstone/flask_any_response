# UDP test

## Build
- Server simple
```bash
python3 main_server.py;
```
- Server enviroment
```bash
# install
python3 -m virtualenv venv;
source venv/bin/activate;
pip3 install -r requirements.txt;

# alternative
export APP_PATH='./';
export GUNICORN_MODULE='main';
bash entrypoint.sh;
```
- Client
```bash
python3 main_client.py;
```
- Client nmap
```bash
sudo nmap -Pn -sU -P0 127.0.0.1 -p 5005;
```

## Build annd run
```bash
# build
docker build -t poxstone/udpserver:latest .;
# run
docker run --rm -it --name udpserver --net host -e UDP_PORT=5006 -p "5006:5006/udp" poxstone/udpserver:latest;
# production
docker run -itd --restart always --net host -e VERSION_DEP=MAIN -e UDP_PORT=5006 -p "5006:5006/udp" poxstone/udpserver:latest;
```

```bash
docker push poxstone/udpserver:latest;
```
