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
# alternative gunicorn (comment TLS --certfile and --keyfile)
gunicorn --workers="2" --timeout="120" --bind="0.0.0.0:8080" --certfile=".certs/tls.crt" --keyfile=".certs/tls.key" main:app;
```

- Docker
```bash
docker build -t poxstone/flask_any_response .;
docker push poxstone/flask_any_response;
# local
docker run --rm -it --net host -p 80:80 -p 9090:9090/tcp -p 9191:9191 -p 8080:8080 -p 5005:5005/udp -p 5678:5678 -p 50051:50051 -e GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT}" poxstone/flask_any_response;
# run certs
docker run --rm -it --net host -p 8080:8080 -v "${PWD}/.certs-self/:/app/.certs/" -e "CERTFILE_CRT=.certs/tls.crt" -e "KEYFILE_TLS=.certs/tls.key" poxstone/flask_any_response;
# production
docker run -itd --pull=always --restart always --net host -e VERSION_DEP=MAIN -p 9090:9090/tcp -p 80:80 -p 9191:9191 -p 5678:5678 -p 8080:8080 -p 5005:5005/udp -p 50051:50051 -e GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT}" poxstone/flask_any_response;
```
- Simple k8s
```bash
# Run normal
kubectl run test-app --image=poxstone/flask_any_response --port=8080 --labels="app=flask,env=dev" -n default-a;

# Run Interactive
kubectl run -i -t test-tty --image=poxstone/flask_any_response --restart=Never -- sh;
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

### k8s and ssl cert

- Variables
```bash
export service="fla-service-a";
export secret="fla-secret-service-a";
export namespace="default-a";

export csrName="${service}.${namespace}";
#export tmpdir="$(mktemp -d)";
export tmpdir=".certs-self";
mkdir -p ${tmpdir};
echo "${tmpdir}";

# for run python
export GRPC_HOST="${service}.${namespace}.svc";
export CERTFILE_CRT="${tmpdir}/tls.crt";
export KEYFILE_TLS="${tmpdir}/tls.key";
export CHAIN_PEM="${tmpdir}/chain.pem";
export GRPC_PORT="50051";
```

- Self-signed works for grpc
```bash
cat > ${tmpdir}/csr.conf <<EOF
[req]
default_bits = 2048
distinguished_name = req_distinguished_name
default_md = sha256
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
C = US
ST = California
L = San Fransisco
O = FlaskAny
OU = FlaskAny Dev
CN = ${service}.${namespace}.svc

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = ${service}.${namespace}.svc
DNS.2 = ${service}.${namespace}.svc.cluster.local
DNS.3 = ${service}
DNS.2 = *.default-b.svc.cluster.local
DNS.2 = *.default-c.svc.cluster.local
DNS.2 = *.default-z.svc.cluster.local
DNS.5 = *.minikube.com
IP.1 = 127.0.0.1
IP.2 = 10.109.16.167
IP.2 = 192.168.49.2
EOF
openssl genpkey -algorithm RSA -out ${KEYFILE_TLS};
openssl req -new -x509 -days 365 -key ${KEYFILE_TLS} -out ${CERTFILE_CRT} -config ${tmpdir}/csr.conf;
cat ${CERTFILE_CRT} ${KEYFILE_TLS} > ${CHAIN_PEM};
```

- k8s-signed
```bash
cat <<EOF >> ${tmpdir}/csr.conf
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = ${service}
DNS.2 = ${service}.${namespace}
DNS.3 = ${service}.${namespace}.svc
EOF

# private key
openssl genrsa -out "${KEYFILE_TLS}" 2048;

# certified request
openssl req -new -key "${KEYFILE_TLS}" -subj "/CN=${service}.${namespace}.svc" -out "${tmpdir}/server.csr" -config "${tmpdir}/csr.conf";
kubectl delete csr "${csrName}";

# create signature request
cat <<EOF | kubectl create -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: ${csrName}
  namespace: ${namespace}
spec:
  groups:
  - system:authenticated
  request: $(cat ${tmpdir}/server.csr | base64 | tr -d '\n')
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - digital signature
  - key encipherment
  - server auth
EOF

kubectl describe csr "${csrName}";
kubectl get csr "${csrName}" -o yaml;
# approve
kubectl certificate approve "${csrName}";
serverCert=$(kubectl get csr ${csrName} -o jsonpath='{.status.certificate}');
echo $serverCert;
# signed cert
echo ${serverCert} | openssl base64 -d -A -out ${CERTFILE_CRT};
# chain for client
cat ${CERTFILE_CRT} ${KEYFILE_TLS} > ${CHAIN_PEM};
```

- Create k8s secret
```bash
# upload as secret
kubectl create secret generic "${secret}" --from-file=tls.key=${KEYFILE_TLS} --from-file=tls.crt=${CERTFILE_CRT} --from-file=chain.pem=${CHAIN_PEM} --dry-run=client \
        -o yaml | kubectl -n ${namespace} apply -f -

# alternative
kubectl create secret tls "${secret}-tls" --key=${KEYFILE_TLS} --cert=${CERTFILE_CRT}
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
# auto inject (optional)
# 
# inject istio in deployments
istioctl kube-inject -f "../kubernetes/deployment-a.yaml" -o "./deployment-a-withistio.yaml";
istioctl kube-inject -f "../kubernetes/deployment-b.yaml" -o "./deployment-b-withistio.yaml";

# run kiali
kubectl port-forward -n istio-system deployment/kiali 20001:20001

# deploy
kubectl apply -f "./";
```
### Istio kinds
- **Gateway**: Istio Load Balancer (L4)
  - istio/istio-raw/gateway_virtualServices/
    - Edit virtualService.yaml to configure gateway out and weigth services
    - Edit gateway.yaml to bind svc istio LoadBalancer
  - Copy EXTERNAL-IP from: `kubectl get svc istio-ingressgateway -n istio-system`
  - Connect to pod: `kubectl get exec -it $(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep service-a) -n istio-system`
    - Do curl into POD to istio-ingressgateway `curl EXTERNAL-IP`
- **VirtualService**: Split traffict to services and output to gateway
  - istio/istio-raw/gateway_virtualServices/
  - Like GateWay...
- **AuthorizationPolicy**: is like Firewall, Allow authorize traffict between services, namespaces, ips, servicesAccounts
  - istio/istio-raw/authorizationPolicy/
  - Edit authorizationPolicy.yaml
- **RequestAuthentication**: Add encription to requests
- **ServiceEntry**: 
  - istio/istio-raw/serviceEntry/
  - Edit serviceEntry.yaml to change consult endpoints
  - kiali: `istioctl dashboard kiali`
  - `for i in {0..3000};do curl -X POST "${URL}/json-requests/1" -H "Content-Type: application/json" -d '@./curl_tests/json-requests_serviceEntry.json';done;`
- **PeerAuthentication**: Implements automatic mtls into namespace deployed
  - Like ServiceEntry
  - Edit istio/istio-raw/serviceEntry/peerAuthentication.yaml
- **IstioOperator**: is self the istio config in istio-system, plugins enabled and anothers
  - `kubectl edit IstioOperator installed-state -n istio-system`
- **EnvoyFilter**: Allow modify behavior "Evoy proxy sidecard" of all pods. like rate_limit
- **ProxyConfig**: Allow config anothers properties of EnvoyPorxy like timeout, protocols, dns...
- **FrontendConfig**:
- **DestinationRule**:: service comunication
- **DestinationRule**:
- **Telemetry**:
- **WorkloadEntry**:
- **WorkloadGroup**:


Ingress (gce) > istio-ingressgateway (backend)

### Gateway (Istio)

#### GKE (Service mesh)
> [Deploying Gateways](https://cloud.google.com/kubernetes-engine/docs/how-to/deploying-gateways)
* Require deplyment-a.yaml and service-a.yaml
```bash
cd istio/gke;
kubeclt apply -f gateway-gke-l7-gxlb.yaml -f httproute-a.yaml;
kubectl get gateways;
# copy external ip
curl -H 'host: my.domain1.com' http://${GATEWAY_IP};
```

#### Manual istio install
> [Installing and upgrading gateways](https://cloud.google.com/service-mesh/docs/gateways)
* Require deplyment-a.yaml and service-a.yaml
```bash
cd istio/gke;
istioctl install;
kubectl get service -n istio-system;  # appearce 2 items only
kubectl label namespace default-a istio-injection=enabled;
# recrate pods of deployments
istioctl analyze;
kubectl -n istio-system get controlplanerevision;  # only response -- error: the server doesn't have a resource type "controlplanerevision"
# install gateways and virtualservice
kubectl apply -f gateway-a.yaml -f virtualservice-a.yaml;
# get IP
kubectl get svc istio-ingressgateway -n istio-system;
# copy external ip
curl http://${GATEWAY_IP}:80;
```
#### Google service Mesh (manual istio-ingress)
> [Migrating from Istio on GKE to Anthos Service Mesh](https://cloud.google.com/istio/docs/istio-on-gke/migrate-to-anthos-service-mesh)
- **Currently not working**
- * Require deplyment-a.yaml and service-a.yaml
```bash
cd istio/istio-ingressgateway;
kubectl label namespace default-a istio-injection=enabled;
kubectl apply -f serviceaccount.yaml -f serviceaccount.yaml -f pdb-v1.yaml -f deployment.yaml -fservice.yaml;
```


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
gcloud run deploy fla-response-a --image "gcr.io/${GOOGLE_CLOUD_PROJECT}/flask_any_response"
gcloud run deploy 
```
### cloud run - Yaml
```bash
cd cloudrun;
gcloud run services replace "service-fla-response-a.yaml" --project "${GOOGLE_CLOUD_PROJECT}" --region "us-central1";
gcloud run services replace "service-fla-response-b.yaml" --project "${GOOGLE_CLOUD_PROJECT}" --region "us-central1";
```

## Cloud build

### cloud build - commandline
```bash
cd cloudrun;
gcloud builds submit --config="./cloudbuild.yaml" --region "us-central1" --project "${GOOGLE_CLOUD_PROJECT}";
```

## Minikube and istio

```bash
#start A
minikube start "cluster-1" --cpus='6' --memory='8192' --nodes='1' --kubernetes-version='1.26.3' --addons='ingress-dns,ingress,dashboard,metrics-server';
#start B (potional 3 nodes)
minikube start "cluster-1" --cpus='2' --memory='3072' --nodes='3' --disk-size='8GB' --kubernetes-version='1.26.3' --addons='ingress-dns,ingress,dashboard,metrics-server,freshpod' --subnet='192.168.49.0/24' --network='minikube' --driver='docker' --mount-string="$PWD/mount:/mount" --mount;

minikube addons enable ingress-dns;
minikube addons enable ingress;
minikube addons enable metrics-server;
minikube addons enable registry;
minikube start --embed-certs;

kubectl config set-context --current --namespace=default-a;
# minikube mount "$PWD/.certs:/certs";

istioctl install --set components.egressGateways[0].name=istio-egressgateway --set components.egressGateways[0].enabled=true;
kubectl apply -f https://raw.githubusercontent.com/istio/istio/master/samples/addons/prometheus.yaml;
kubectl apply -f https://raw.githubusercontent.com/istio/istio/master/samples/addons/kiali.yaml;
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.17/samples/addons/grafana.yaml;
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.17/samples/addons/jaeger.yaml;
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.17/samples/addons/extras/zipkin.yaml;
# for sing certs
#kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.11.0/cert-manager.yaml;

# ingress and egress
kubectl label namespace default-a istio-injection=enabled;
minikube dashboard;
istioctl dashboard kiali;
istioctl dashboard prometheus;
istioctl dashboard grafana;
istioctl dashboard jaeger;
istioctl dashboard zipkin;
# important for EXTERNAL IPS
minikube tunnel;

# int previous not works
# rm -rf ${HOME}/.minikube;
```

## Tests
- get parameters: sleep=10&status=502&view=simple&logs=false
> ***GET parameters***:
> - path: use for send aditional path ex: "?path=/administrative/portal"
> - method: use for change method ex: "?method=POST"

```bash
export URL="http://localhost:8080";
```
> If requet requires a TLS cert selfsign use: curl "${URL}" --cacert .certs-self/chain.pem

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
curl -X GET "${URL}/udp-requests/localhost/5005?MESSAGE=hola";

# grpc test
curl -iLX GET "${URL}/grpc-requests/127.0.0.1/50051";
curl -iLX POST "${URL}/grpc-requests/127.0.0.1/50051" -H "Content-Type: application/json" -d '{"user_name":"Carl Sagan", "age": "42", "email": "John_doe@mail.com"}';

# proxy request GET external html request
curl -X GET "${URL}/requests/https/eltiempo.com/443?path=/opinion/columnistas/martha-senn&other=none";

# proxy request POST test API (curl -k -X POST https://jsonplaceholder.typicode.com/posts -H "Content-Type: application/json" -d '{"hola":"perro"}')
curl -X POST "${URL}/requests/https/jsonplaceholder.typicode.com/443?path=/posts" -H "Content-Type: application/json" -d '{"hola":"perro"}';

# multiple curls
curl -X POST "${URL}/json-requests/1" -H "Content-Type: application/json" -d '[{"url":"https://jsonplaceholder.typicode.com/posts", "method":"POST", "body":{"hola": "perro"}, "headers":{"Content-Type": "application/json"}}, {"url":"https://jsonplaceholder.typicode.com/posts", "method":"POST", "body":{}, "headers":{"Content-Type": "application/json"}}]';

# nested curls json
for i in {0..3000};do sleep 5;curl -X POST "${URL}/json-requests/1" -H "Content-Type: application/json" -d '@./curl_tests/json-requests_k8s.json';done;
# time data
for i in {0..3000};do sleep 2;curl -w "@./curl_tests/curl-format.txt" -o /dev/null -s -X POST "${URL}/json-requests/1/" -H "Content-Type: application/json" -d '@./curl_tests/json-requests_k8s.json';done;

# request concat, this is used with similar containers redirection trafict in much services
curl -X GET "${URL}/concat-requests/1?hosts=http://localhost:8080/,http://localhost:8080";

# note remove scape slash for browser
# proxy request POST with GET test API (parameter method=POST body=\{\"hola\":\"mundo\"\})
curl -X GET "${URL}/requests/https/jsonplaceholder.typicode.com/443?path=/posts&method=POST&body=\{\"hola\":\"mundo\"\}&headers=\{\"Content-Type\":\"application/json\"\}";
# get token
curl -X GET "${URL}/requests/http/metadata.google.internal/80?path=/computeMetadata/v1/instance/service-accounts/default/token&method=GET&headers=\{\"Content-Type\":\"application/json\",\"Metadata-Flavor\":\"Google\"\}";
# get vm lists: /requests/https/compute.googleapis.com/443?path=/compute/v1/projects/my-gcp-project/zones/us-east1-b/instances&method=GET&headers={"Content-Type":"application/json","Authorization":"Bearer ya29.c...."}
curl -X GET "${URL}/requests/https/compute.googleapis.com/443?path=/compute/v1/projects/${GOOGLE_CLOUD_PROJECT}/zones/us-east1-b/instances&method=GET&headers=\{\"Content-Type\":\"application/json\",\"Authorization\":\"Bearer%20ya29.c...\"\}";


curl -X POST "${URL}/do/script/" -H "Content-Type: application/json"  -d '{"command":"curl  -H \"Metadata-Flavor: Google\" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"}'
# proxy request POST with GET test API (parameter method=GET https://jsonplaceholder.typicode.com:443/comments?params=postId=1,sort=first)
curl -X GET "${URL}/requests/https/jsonplaceholder.typicode.com/443?path=/comments&method=GET&params=postId=1,sort=first";

# simple ping (for validate)
curl -X GET "${URL}/ping/8.8.8.8";

# mime-types (css,txt,html,js,pdf,image,bin)
curl -X GET "${URL}/my_file.css";
# => mime_type = text/css

# generate downloable file (1M | 1G | 1T...)
curl -X GET "${URL}/download/1M" --output "bigfile.bin";

# some bash commands by exec
curl -X POST "${URL}/do/com" -H "Content-Type: application/json" -d '{"command":["ping","-c","2","8.8.8.8"]}';
curl -X POST "${URL}/do/com" -H "Content-Type: application/json" -d '{"command":["nmap","localhost"]}';
curl -X POST "${URL}/do/com" -H "Content-Type: application/json" -d '{"command":["dig","google.com"]}';
curl -X POST "${URL}/do/com" -H "Content-Type: application/json" -d '{"command":["mysql", "-u", "root", "-h", "34.74.45.17", "-pMyPass", "-D", "cloudkey", "-e", "select * from users"]}';
# redis response PONG if is well 
curl -X POST "${URL}/do/script" -H "Content-Type: application/json" -d '{"command":"redis-cli -h 10.18.241.3 -p 6379 PING"}';
# redis get command
curl -X POST "${URL}/do/script" -H "Content-Type: application/json" -d '{"command":"echo \"KEYS *\" | redis-cli -h 10.18.224.3 -p 6379"}';
# sql server connect
curl -X POST "${URL}/do/script" -H "Content-Type: application/json" -d '{"command":"sqlcmd -S 34.133.118.251 -U sqlserver -P MyPASS -b -Q \"SELECT Name from sys.databases;\""}';
# some bash commands by bash script (more support)
curl -X POST "${URL}/do/script" -H "Content-Type: application/json" -d '{"command":"date > date.txt; ls;cat date.txt"}';
# set DS hosts (don't works)
curl -X POST "${URL}/do/script" -H "Content-Type: application/json" -d '{"command":"echo \"my.domain1.com 192.168.49.2\" >> /etc/hosts"}';

# test redirction 302 simple relative
curl -X GET -kLI "${URL}/redirect-relative";

# test redirction 302 custom absolute
curl -X GET -kLI "${URL}/redirect-absolute/https/eltiempo.com/443?path=/opinion/columnistas/martha-senn";

# test smtp
curl -X GET "${URL}/testsmtp/smtp.gmail.com:587/user@comain.com/MyPasswd";

# tests stress --time (cloud run not works)
curl -X POST "${URL}/do/script" -H "Content-Type: application/json" -d '{"command":"stress-ng --cpu 1 --vm-bytes 128M"}';
curl -X POST "${URL}/do/script" -H "Content-Type: application/json" -d '{"command":"stress-ng -c 1 -i 1 -m 1 --vm-bytes 128M -t 10s"}';

# cloud run metadata curl get token
curl -X POST "${URL}/do/script" -H "Content-Type: application/json"  -d '{"command":"curl  -H \"Metadata-Flavor: Google\" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"}'

# basic authentication
curl -X POST "${URL}/do/script" -H "Content-Type: application/json" -d '{"command":"curl -u 'usuario1:contrasenia1'"}';

# use authorization with curl
-H "Authorization: Bearer ya29.a..."
-H "Authorization: Basic bG9naW4..."

# function
function sc { curl -X POST -kiL "${2}/do/script" -H "Content-Type: application/json" -d "{\"command\":\"${1}\"}"; };
# ping ipv6
sc "curl -6 'http://[2600:1901:0:38c4::]:80'" "${URL}";
sc "curl '$URLlb "${URL1}";
```

## Websocket (ws wss http https)
- Browser: http://127.0.0.1:8080/socket-requests/ws/localhost/5678/client-2.html
  - protocol: ws wss ( http - https for another tests) 
  - host: domain or ip
  - port: port expose server 5678
  - path: client-1.html (chancge number or anything)
- nodejs: 
  - `npm install -g wscat`
  - `wscat -c "ws://localhost:5678"`

```bash
curl --include 
     --no-buffer 
     --header "Connection: Upgrade" \
     --header "Upgrade: websocket" \
     --header "Host: localhost:5678" \
     --header "Origin: http://localhost:5678" \
     --header "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
     --header "Sec-WebSocket-Version: 13" \
     "http://localhost:5678/socket-requests/ws/localhost/5678/client-2.html"

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
siez
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
var req_path = `${location.origin}/do/script`;
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
sudo chown -R "$(id -u):$(id -g)" ${HOME}/cerbot;
cd ${HOME}/cerbot/archive/${MY_DOMAIN}/;
```
4. Keys into folder:
> X0= Principal domain, X1=ISRG Root X1, X2= DST Root CA X3
  - **cert1.pem** (cert.pem, tls.crt x0): PEM encoded X.509 public key, certificate. Into kubernetes secret values are **tls.crt** but in base 64 (BEGIN CERTIFICATE X 1 cert)
  - **chain1.pem** (chain.pem X1, X2): us not cert1.pem  conecta el certificado emitido por la CA con el certificado raíz de la CA, se utiliza en el cliente/browser/navegador cuando este no puede conectar con el CA (BEGIN CERTIFICATE X2 chains)
  - **fullchain.pem** (fullchain.pem, tls.crt X0, X1, X2): has X.509 and intermedium cert is better than cert1.pem (BEGIN CERTIFICATE X3 certs)
  - **privkey1.pem** (privkey.pem, tls.key): unencrypted PEM encoded RSA, private key. Into kubernetes secret values are **tls.key** but in base 64 (BEGIN PRIVATE KEY X1 Private Key backend)
5. Keys for kubernetes secret (secret-ssl-fla-service)
```bash
# tls.crt and tls.key
ln -s ./cert1.pem "tls.crt";
ln -s ./privkey1.pem "tls.key";

kubectl create secret generic secret-main-domain-tls --from-file="./.certs/tls.crt" --from-file="./.certs/tls.key" --from-file="./.certs/chain.pem";
# get keys
kubectl get secrets ssl-temp -o yaml;
```
6. Paste base64 values **tls.crt** and **tls.key** into **secret-main-domain-tls.yaml** and deploy with kubectl
```bash
kubectl apply -f "secret-main-domain-tls.yaml";
```
7. Edit ingress-a.yaml and ensure:
```yaml
...
spec:
  tls:
  - hosts:
    - my.domain1.com
    secretName: secret-ssl-fla-service
...
```
8. Apply ingress and wait
```bash
kubectl applly -f "ingress-a.yaml";
# get ingress status
kubectl describe ingress fla-service-a-ingress;

```
## supported requests

- initialDelaySeconds: 20
- periodSeconds: 15
- successThreshold: 1
- timeoutSeconds: 60

| config                    | cpu-init | cpu-min | cpu-max | ram-init | ram-min | ram-max | request-sim | request-max |
| ------------------------- | -------- | ------- | ------- | -------- | ------- | ------- | ----------- | ----------- |
| 1replica, 1worker         | 51m      | 4m      | ---     | ---      | 74Mi    | ---     | 1           | ---         |
| 1replica, 2worker         | 51m      | 16m     | 3045m   | ---      | 90Mi    | 106Mi   | 2           | ---         |
| 1replica, 10worker        | 103m     | 4m      | ---     | ---      | 218Mi   | ---     | 10          | ---         |
| 1replica, 1worker,  istio | ---      | 12m     | ---     | ---      | 118Mi   | ---     | 1           | ---         |
| 1replica, 2worker,  istio | 70m      | 8m      | 3045m   | 132Mi    | 134Mi   | 153Mi   | 2 45/1.5min | 259rpms     |
| 1replica, 10worker, istio | 102m     | 8m      | ---     | ---      | 260Mi   | ---     | 10          | ---         |

