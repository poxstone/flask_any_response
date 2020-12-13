# UDP test

## Build
- Server simple
```bash
python3 main.py;
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
python3 receiving.py;
```
- Client nmap
```bash
sudo nmap -Pn -sU -P0 -v felix 127.0.0.1 -p 5005;
```

## Build annd run
```bash
# build
docker build -t poxstone/udpserver:latest .;
# run
docker run --rm -it --name udpserver --net host -p "5005:5005/udp" poxstone/udpserver:latest;
# production
docker run -itd --restart always --net host -e VERSION_DEP=MAIN -p "5005:5005/udp" poxstone/udpserver:latest;
```