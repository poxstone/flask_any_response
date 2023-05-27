# Simple GRPC Python 3

## Chat GPT promt
 ```text
Requiero hacer un servicio "userexample" utilizando grpc con python3, dame un ejemplo de como hacerlo y qué librerias debo utilizar. El servicio tener campos de: user_name, age, email.

Dame un ejemplo para probar el metodo "GetUser" que se encuentra en el archivo de servidor con el tipo de objeto que devería de devolver.
```
## Enviroment
- Enable enviroment and libraries:
```bash
python3 -m virtualenv venv;
source venv/bin/activate;
pip install -r requirements.txt;
```

- Create service_pb2_grpc.py service_pb2.py from service.proto:
```bash
cd ./proto_grpc/;
python -m grpc_tools.protoc -I ./ --python_out=. --grpc_python_out=. userexample.proto;
```

## Test service python

- Server
```bash
python3 main_server.py;
```

- Client python
```bash
python3 main_client.py;
# optional arguments in order
python3 main_client.py 'local.poxsilver5.store' '50051' './.certs/tls.crt' './.certs/tls.key' './.certs/chain.pem';
```


- Client grpcurl
| [Documentation - github](https://github.com/fullstorydev/grpcurl)

```bash

# download protoc (for generate index from .proto) https://grpc.io/docs/protoc-installation/
PB_REL="https://github.com/protocolbuffers/protobuf/releases";
curl -LO "$PB_REL/download/v3.15.8/protoc-3.15.8-linux-x86_64.zip";
unzip "protoc-3.15.8-linux-x86_64.zip";
./protoc/bin/protoc --proto_path=. --descriptor_set_out=userexample.protoset --include_imports userexample.proto
```

```bash
# download grpcurl https://github.com/fullstorydev/grpcurl/releases
curl -LO "https://github.com/fullstorydev/grpcurl/releases/download/v1.8.7/grpcurl_1.8.7_linux_x86_64.tar.gz";
tar -xvzf "grpcurl_1.8.7_linux_x86_64.tar.gz";

# describe proto
grpcurl -protoset my-protos.bin describe my.custom.server.Service.MethodOne

# get curls
grpcurl -plaintext localhost:50051 describe userexample.UserExampleService;

grpcurl -plaintext -d '{"user_name": "John Doe"}' localhost:50051 userexample.UserExampleService/GetUser

grpcurl -plaintext localhost:50051 userexample.UserExampleService/GetUser

```

### Test service python
