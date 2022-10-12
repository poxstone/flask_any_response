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
docker push poxstone/flask_any_response;
# local
docker run --rm -it --net host -p 80:80 -p 9090:9090/tcp -p 9191:9191 -p 8080:8080 -p 5005:5005/udp -p 5678:5678 -e GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT}" poxstone/flask_any_response;
# production
docker run -itd --pull=always --restart always --net host -e VERSION_DEP=MAIN -p 9090:9090/tcp -p 80:80 -p 9191:9191 -p 5678:5678 -p 8080:8080 -p 5005:5005/udp -e GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT}" poxstone/flask_any_response;
```

# to GCP by tag
```bash
# loging
gcloud auth configure-docker;
# change tag (optional)
docker tag "poxstone/flask_any_response" "gcr.io/${GOOGLE_CLOUD_PROJECT}/flask_any_response";
docker push "gcr.io/${GOOGLE_CLOUD_PROJECT}/flask_any_response";

# Build direct to GCP
gcloud builds submit --tag "gcr.io/${GOOGLE_CLOUD_PROJECT}/flask_any_response";

```
- Publish
```bash
docker push poxstone/flask_any_response:latest;
```

## Kubernetes
```bash
cd kubernetes;
kubectl apply -f ./;
```

## Helm
```bash
cd  helm;
helm upgrade --install flaskanyresponse-helm flaskanyresponse-helm/;

# delete
helm uninstall flaskanyresponse-helm;
```
## Istio
```bash
cd ./istio;
# install istio into cluster
istioctl install;

# inject istio in deployments
istioctl kube-inject -f ../kubernetes/deployment-a.yaml -o ./deployment-a-withistio.yaml;
istioctl kube-inject -f ../kubernetes/deployment-b.yaml -o ./deployment-b-withistio.yaml;

# deploy
kubectl apply -f ./;
```

## App Engine

### appengine standard
- [appengine standard](https://cloud.google.com/appengine/docs/standard/python3/runtime)
- [hello_world](https://cloud.google.com/appengine/docs/standard/python3/runtime)

```bash
gcloud app deploy --appyaml="app_standard.yaml" --project="${GOOGLE_CLOUD_PROJECT}"
gcloud app browse;
```

### appengine flex
- [appengine standard](https://cloud.google.com/appengine/docs/standard/python3/runtime)
- [hello_world](https://cloud.google.com/appengine/docs/standard/python3/runtime)

```bash
gcloud app deploy --appyaml="app_flex.yaml" --project="${GOOGLE_CLOUD_PROJECT}"
gcloud app browse;
```

## Cloud Run

### cloud run - command
```bash
gcloud run deploy flask-any-response-a --image "gcr.io/${GOOGLE_CLOUD_PROJECT}/flask_any_response"
gcloud run deploy 
```
### cloud run - Yaml
```bash
cd cloudrun;
gcloud run services replace service-flask-any-response-a.yaml --project "${GOOGLE_CLOUD_PROJECT}" --region us-central1;
gcloud run services replace service-flask-any-response-b.yaml --project "${GOOGLE_CLOUD_PROJECT}" --region us-central1;
```

## Cloud build

### cloud build - commandline
```bash
cd cloudrun;
gcloud builds submit --config="./cloudbuild.yaml" --region "us-central1" --project "${GOOGLE_CLOUD_PROJECT}" --region us-central1;
```


## Tests
> ***GET parameters***:
> - path: use for send aditional path ex: "?path=/administrative/portal"
> - method: use for change method ex: "?method=POST"

```bash

export URL="http://localhost:8080";
```

```bash
# blank print for healthcheck tests set env PATH_IGNORE= "favicon.ico,blank,echo.php,proxy.php"
curl -X GET "${URL}/blank";

export
# levels
curl -X GET "${URL}/lv1/lv2";
curl -X POST "${URL}/lv1/lv2";

# udp send
curl -X GET "${URL}/testudp/?UDP_IP=127.0.0.1&UDP_PORT=5005&MESSAGE=hola";

# proxy request GET external html request
curl -X GET "${URL}/requests/https/eltiempo.com/443/?path=/opinion/columnistas/martha-senn&other=none";

# proxy request POST test API (curl -k -X POST https://jsonplaceholder.typicode.com/posts -H "Content-Type: application/json" -d '{"hola":"perro"}')
curl -X POST "${URL}/requests/https/jsonplaceholder.typicode.com/443/?path=/posts" -H "Content-Type: application/json" -d '{"hola":"perro"}';

# proxy request POST with GET test API (parameter method=POST body=\{\"hola\":\"mundo\"\})
curl -X GET "${URL}/requests/https/jsonplaceholder.typicode.com/443/?path=/posts&method=POST&body=\{\"hola\":\"mundo\"\}";

# simple ping (for validate)
curl -X GET "${URL}/ping/8.8.8.8";

# mime-types (css,txt,html,js,pdf,image,bin)
curl -X GET "${URL}/my_file.css";
# => mime_type = text/css

# some bash commands by exec
curl -X POST "${URL}/do/com/" -H "Content-Type: application/json" -d '{"command":["ping","-c","2","8.8.8.8"]}';
curl -X POST "${URL}/do/com/" -H "Content-Type: application/json" -d '{"command":["nmap","localhost"]}';
curl -X POST "${URL}/do/com/" -H "Content-Type: application/json" -d '{"command":["dig","google.com"]}';
curl -X POST "${URL}/do/com/" -H "Content-Type: application/json" -d '{"command":["mysql", "-u", "root", "-h", "34.74.45.17", "-pMyPass", "-D", "cloudkey", "-e", "select * from users"]}';
# redis response PONG if is well 
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json" -d '{"command":"redis-cli -h 10.18.241.3 -p 6379 PING"}';
# redis get command
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json" -d '{"command":"echo \"KEYS *\" | redis-cli -h 10.18.224.3 -p 6379"}';
# sql server connect
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json" -d '{"command":"sqlcmd -S 34.133.118.251 -U sqlserver -P MyPASS -b -Q \"SELECT Name from sys.databases;\""}';
# some bash commands by bash script (more support)
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json" -d '{"command":"date > date.txt; ls;cat date.txt"}';

# test redirction 302 simple relative
curl -X GET -kLI "${URL}/redirect/relative";

# test redirction 302 custom absolute
curl -X GET -kLI "${URL}/redirect/absolute/https/eltiempo.com/443?path=/opinion/columnistas/martha-senn";

# test smtp
curl -X GET "${URL}/testsmtp/smtp.gmail.com:587/user@comain.com/MyPasswd";

# tests stress --time (cloud run not works)
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json" -d '{"command":"stress-ng --cpu 1 --vm-bytes 128M"}';
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json" -d '{"command":"stress-ng -c 1 -i 1 -m 1 --vm-bytes 128M -t 10s"}';

# cloud run metadata curl get token
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json"  -d '{"command":"curl  -H \"Metadata-Flavor: Google\" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"}'

# basic authentication
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json" -d '{"command":"curl -u 'usuario1:contrasenia1'"}';

# use authorization with curl
-H "Authorization: Bearer ya29.a..."
-H "Authorization: Basic bG9naW4..."


# function
function sc { curl -X POST -kiL "${2}/do/script/" -H "Content-Type: application/json" -d "{\"command\":\"${1}\"}"; };
# ping ipv6
sc "curl -6 'http://[2600:1901:0:38c4::]:80'" "${URL}";
sc "curl '$URLlb "${URL1}";
```

## websocket
- Browser: http://localhost:8080/web-socket.html?port=5678&host=localhost
- nodejs: 
  - `npm install -g wscat`
  - `wscat -c "ws://localhost:5678"`

```bash
curl --include 
     --no-buffer 
     --header "Connection: Upgrade" \
     --header "Upgrade: websocket" 
     --header "Host: localhost:5678" 
     --header "Origin: http://localhost:5678" 
     --header "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" 
     --header "Sec-WebSocket-Version: 13" 
     "http://localhost:5678/"

curl 'http://localhost:5678/' \
  -H "Connection: Upgrade" \
  -H 'Pragma: no-cache' \
  -H 'Origin: http://localhost:5678' \
  -H 'Sec-WebSocket-Key: IxtOwIPwOjTwA8OAGmtWSA==' \
  -H 'Upgrade: websocket' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: Upgrade' \
  -H 'Sec-WebSocket-Version: 13' \
  -H 'Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits' \
  --include \
  --no-buffer \
  --compressed \
  --connect-timeout 300 \
  --max-time 300 \
  --output "websocket.txt";
  # other TTY
  tail -f websocket.txt;
```


## Utils

- (Setting up an internal HTTP(S) load balancer with Cloud Run)[https://console.cloud.google.com/net-services/loadbalancing/details/internalRegionalHttp/us-central1/urlmap-oscar-run-internal]

## Browser requests test
- Simple request
```javascript
for (let i=0;i<10;i++) { fetch(`${location.href}?i=${i}`); }
```

- Interval request
```javascript
/* Test req/s */
var num_requests = 18;  // req per 1 sec
var sec_interval= 1*1000; // each 1 sec
var count_until = 180; // 180 sec
var count = 0;
// simple request
var req_path = `${location.origin}/my_page`;
var req_cont =  {
  "headers": {"cache-control":"max-age=10000"},
  "method": "GET",
};
// great request
var req_path = `${location.origin}/do/script/`;
var req_cont =  {
  "headers": {"cache-control":"max-age=10000", "Content-Type":"application/json"},
  "method": "POST",
  "body": JSON.stringify({messaje:'my_mesaje', command:'sleep 1'}),
};


setInterval(() => {for (let i=0;i<=num_requests;i++) {if (count <= count_until) { fetch(`${req_path}?i=${i}&c=${count}`, req_cont);count=i<num_requests?count:count+1;} } }, sec_interval);
```