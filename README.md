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

# simper 302 redirect
curl -X GET -ikL "${URL}/redirect/relative";

# redirect absolute
curl -X GET -ikL "${URL}/redirect/absolute/https/google.com/443";

# some bash commands by exex
curl -X POST "${URL}/do/com/" -H "Content-Type: application/json" -d '{"command":["ping","-c","2","8.8.8.8"]}';
curl -X POST "${URL}/do/com/" -H "Content-Type: application/json" -d '{"command":["nmap","localhost"]}';
curl -X POST "${URL}/do/com/" -H "Content-Type: application/json" -d '{"command":["mysql", "-u", "root", "-h", "34.74.45.17", "-pMyPass", "-D", "cloudkey", "-e", "select * from users"]}';
# some bash commands by bash script (more support)
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json" -d '{"command":"date > date.txt; ls;cat date.txt"}';

# tests stress --time (cloud run not works)
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json" -d '{"command":"stress-ng --cpu 1 --vm-bytes 128M"}';
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json" -d '{"command":"stress-ng -c 1 -i 1 -m 1 --vm-bytes 128M -t 10s"}';

# cloud run metadata curl get token
curl -X POST "${URL}/do/script/" -H "Content-Type: application/json"  -d '{"command":"curl  -H \"Metadata-Flavor: Google\" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"}'


-H "Authorization: Bearer ya29.a..."
```