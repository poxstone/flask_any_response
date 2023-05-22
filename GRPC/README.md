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
```


- Client grpcurl
```bash
grpcurl -plaintext localhost:50051 describe userexample.UserExampleService;

grpcurl -plaintext -d '{"user_name": "John Doe"}' localhost:50051 userexample.UserExampleService/GetUser

grpcurl -plaintext localhost:50051 userexample.UserExampleService/GetUser
```

### Test service python
