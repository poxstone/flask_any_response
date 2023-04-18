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

# To GCP by tag
```bash
# loging
gcloud auth configure-docker;
# change tag (optional)
# Container registry
docker tag "poxstone/flask_any_response" "gcr.io/${GOOGLE_CLOUD_PROJECT}/flask_any_response";
docker push "gcr.io/${GOOGLE_CLOUD_PROJECT}/flask_any_response";
# Artifact registry
docker tag "poxstone/flask_any_response" "us-east1-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/repo/flask_any_response";
docker push "us-east1-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/repo/flask_any_response";

# Build direct to GCP
gcloud builds submit --tag "gcr.io/${GOOGLE_CLOUD_PROJECT}/flask_any_response";

```
- Publish
```bash
docker push "poxstone/flask_any_response:latest";
```
## Kubernetes


## Kubernetes

- Derraform (update PROJECT_ID variable)
```bash
cd terraform;
export TF_VAR_PROJECT_ID="${GOOGLE_CLOUD_PROJECT}";
export TF_VAR_PREFIX_APP="flask";
export TF_VAR_REGION_DEFAULT="us-east1";

terraform init;
terraform apply;
gcloud container clusters get-credentials "gke-cluster-${TF_VAR_PREFIX_APP}-01" --zone "${TF_VAR_REGION_DEFAULT}" --project "${GOOGLE_CLOUD_PROJECT}";
```
- Deploy
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
istioctl kube-inject -f "../kubernetes/deployment-a.yaml" -o "./deployment-a-withistio.yaml";
istioctl kube-inject -f "../kubernetes/deployment-b.yaml" -o "./deployment-b-withistio.yaml";

# run kiali
kubectl port-forward -n istio-system deployment/kiali 20001:20001

# deploy
kubectl apply -f "./";
```
Istio kinds:
- Gateway: Load Balancer (L4)
- VirtualService: Service ()
- IstioOperator
- FrontendConfig
- EnvoyFilter
- IstioOperator
- DestinationRule: service comunication
- ServiceEntry


Ingress (gce) > istio-ingressgateway (backend)

### Gateway (Istio)

#### GKE (Service mesh)
> [Deploying Gateways](https://cloud.google.com/kubernetes-engine/docs/how-to/deploying-gateways)
* Require deplyment-a.yaml and service-a.yaml
´´´bash
cd istio/gke;
kubeclt apply -f gateway-gke-l7-gxlb.yaml -f httproute-a.yaml;
kubectl get gateways;
# copy external ip
curl -H 'host: my.domain1.com' http://${GATEWAY_IP};
´´´

#### Manual istio install
> [Installing and upgrading gateways](https://cloud.google.com/service-mesh/docs/gateways)
* Require deplyment-a.yaml and service-a.yaml
´´´bash
cd istio/gke;
istioctl install;
kubectl get service -n istio-system;  # appearce 2 items only
kubectl label namespace default istio-injection=enabled;
# recrate pods of deployments
istioctl analyze;
kubectl -n istio-system get controlplanerevision;  # only response -- error: the server doesn't have a resource type "controlplanerevision"
# install gateways and virtualservice
kubectl apply -f gateway-a.yaml -f virtualservice-a.yaml;
# get IP
kubectl get svc istio-ingressgateway -n istio-system;
# copy external ip
curl http://${GATEWAY_IP}:80;
´´´

## App Engine

### appengine standard
- [appengine standard](https://cloud.google.com/appengine/docs/standard/python3/runtime)
- [hello_world](https://cloud.google.com/appengine/docs/standard/python3/runtime)
- Uncomment "uwsgi==..." from **requirements.txt**

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
gcloud run services replace "service-flask-any-response-a.yaml" --project "${GOOGLE_CLOUD_PROJECT}" --region "us-central1";
gcloud run services replace "service-flask-any-response-b.yaml" --project "${GOOGLE_CLOUD_PROJECT}" --region "us-central1";
```

## Cloud build

### cloud build - commandline
```bash
cd cloudrun;
gcloud builds submit --config="./cloudbuild.yaml" --region "us-central1" --project "${GOOGLE_CLOUD_PROJECT}";
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
# sleep in any get level or url
curl -X GET "${URL}/lv1/lv2?sleep=10";

# udp send
curl -X GET "${URL}/testudp/?UDP_IP=127.0.0.1&UDP_PORT=5005&MESSAGE=hola";

# proxy request GET external html request
curl -X GET "${URL}/requests/https/eltiempo.com/443/?path=/opinion/columnistas/martha-senn&other=none";

# proxy request POST test API (curl -k -X POST https://jsonplaceholder.typicode.com/posts -H "Content-Type: application/json" -d '{"hola":"perro"}')
curl -X POST "${URL}/requests/https/jsonplaceholder.typicode.com/443/?path=/posts" -H "Content-Type: application/json" -d '{"hola":"perro"}';

# multiple curls
curl -X POST "${URL}/json-requests/1/" -H "Content-Type: application/json" -d '[{"url":"https://jsonplaceholder.typicode.com/posts", "method":"POST", "body":{"hola": "perro"}, "headers":{"Content-Type": "application/json"}}, {"url":"https://jsonplaceholder.typicode.com/posts", "method":"POST", "body":{}, "headers":{"Content-Type": "application/json"}}]';

# nested curls json
curl -X POST "${URL}/json-requests/1/" -H "Content-Type: application/json" -d '@./curl_tests/json-requests_local.json';
# option two microservices
for i in {0..300};do curl -X POST "${URL}/json-requests/1/" -H "Content-Type: application/json" -d '@./curl_tests/json-requests_k8s.json';done;
# time data
for i in {0..300};do curl -w "@./curl_tests/curl-format.txt" -o /dev/null -s -X GET "${URL}/json-requests/1/" -H "Content-Type: application/json"  -d '@./curl_tests/json-requests_k8s.json';done;

# request concat, this is used with similar containers redirection trafict in much services
curl -X GET "${URL}/concat-requests/1/?hosts=http://localhost:8080/,http://localhost:8080";

# note remove scape slash for browser
# proxy request POST with GET test API (parameter method=POST body=\{\"hola\":\"mundo\"\})
curl -X GET "${URL}/requests/https/jsonplaceholder.typicode.com/443/?path=/posts&method=POST&body=\{\"hola\":\"mundo\"\}&headers=\{\"Content-Type\":\"application/json\"\}";
# get token
curl -X GET "${URL}/requests/http/metadata.google.internal/80/?path=/computeMetadata/v1/instance/service-accounts/default/token&method=GET&headers=\{\"Content-Type\":\"application/json\",\"Metadata-Flavor\":\"Google\"\}";
# get vm lists: /requests/https/compute.googleapis.com/443/?path=/compute/v1/projects/my-gcp-project/zones/us-east1-b/instances&method=GET&headers={"Content-Type":"application/json","Authorization":"Bearer ya29.c...."}
curl -X GET "${URL}/requests/https/compute.googleapis.com/443/?path=/compute/v1/projects/${GOOGLE_CLOUD_PROJECT}/zones/us-east1-b/instances&method=GET&headers=\{\"Content-Type\":\"application/json\",\"Authorization\":\"Bearer%20ya29.c...\"\}";


curl -X POST "${URL}/do/script/" -H "Content-Type: application/json"  -d '{"command":"curl  -H \"Metadata-Flavor: Google\" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"}'
# proxy request POST with GET test API (parameter method=GET https://jsonplaceholder.typicode.com:443/comments?params=postId=1,sort=first)
curl -X GET "${URL}/requests/https/jsonplaceholder.typicode.com/443/?path=/comments&method=GET&params=postId=1,sort=first";

# simple ping (for validate)
curl -X GET "${URL}/ping/8.8.8.8";

# mime-types (css,txt,html,js,pdf,image,bin)
curl -X GET "${URL}/my_file.css";
# => mime_type = text/css

# generate downloable file (1M | 1G | 1T...)
curl -X GET "${URL}/download/1M" --output "bigfile.bin";

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
# set DS hosts (don't works)
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json" -d '{"command":"echo \"my.domain1.com 192.168.49.2\" >> /etc/hosts"}';

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

## Websocket
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

## Linux requests test

```bash
sudo apt install siege;
# simule 255 concurrents users
sie
ge -c 255 "${URL}";
```
```bash
sudo apt-get install apache2-utils -y;
ab -t 120 -n 50000 -c 1000 "${URL}";
```
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
## Generate let's encrypt certs

1. Run let´s encrypt code (cloud shell works)
```bash
export MY_DOMAIN="my.domain1.com";
# create alias
alias cerbot="docker run --rm -it -p 443:443 -v ${HOME}/cerbot:/etc/letsencrypt -v ${HOME}/cerbot/log:/var/log/letsencrypt quay.io/letsencrypt/letsencrypt:latest";
cerbot certonly --manual -d "${MY_DOMAIN}";
# Follow instructions...
```
2. In another TTY or Browser: Set and get hash/token lets encrypt ${URL} has ${MY_DOMAIN}
```bash
# USE LETS ENCRIPT
# set token with url (also you can use enviroment var LETS_TOKEN)
curl -X GET "http://${MY_DOMAIN}/.well-known/acme-challenge/set/my_return_t0k3nex4mpl3";
# get token (let's encrypt service validate on public url)
curl -X GET "http://${MY_DOMAIN}/.well-known/acme-challenge/t0k3nex4mpl3.from_lets_encrypt";
# output: > my_return_t0k3nex4mpl3
```
3. Go back first TTY and 
```bash
sudo chown -R "$(id -u):$(id -g)" ./cerbot;
cd ./cerbot/archive/${MY_DOMAIN}/;
```
4. Keys into folder:
  - **cert1.pem** (cert.pem, tls.crt): PEM encoded X.509 public key, certificate. Into kubernetes secret values are **tls.crt** but in base 64
  - **chain1.pem** (chain.pem): 
  - **fullchain1.pem** (fullchain.pem): 
  - **privkey1.pem** (privkey.pem, tls.key): unencrypted PEM encoded RSA, private key. Into kubernetes secret values are **tls.key** but in base 64
5. Keys for kubernetes secret (secret-ssl-flask-any-service)
```bash
# tls.crt and tls.key
ln -s ./cert1.pem "tls.crt";
ln -s ./privkey1.pem "tls.key";

kubectl create secret generic ssl-temp --from-file="./tls.crt" --from-file="./tls.key";
# get keys
kubectl get secrets ssl-temp -o yaml;
```
6. Paste base64 values **tls.crt** and **tls.key** into **secret-ssl-a.yaml** and deploy with kubectl
```bash
kubectl applly -f "secret-ssl-a.yaml";
```
7. Edit ingress-a.yaml and ensure:
```yaml
...
spec:
  tls:
  - hosts:
    - my.domain1.com
    secretName: secret-ssl-flask-any-service
...
```
8. Apply ingress and wait
```bash
kubectl applly -f "ingress-a.yaml";
# get ingress status
kubectl describe ingress flask-any-service-a-ingress;
```