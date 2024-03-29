# allow import from previous path
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import grpc
from sys import argv

from proto_grpc import userexample_pb2
from proto_grpc import userexample_pb2_grpc

from application.config import CERTFILE_CRT, KEYFILE_TLS, CHAIN_PEM, GRPC_PORT, GRPC_HOST


GRPC_HOST = argv[1] if len(argv) > 1 else GRPC_HOST
GRPC_PORT = argv[2] if len(argv) > 2 else GRPC_PORT
CERTFILE_CRT = argv[3] if len(argv) > 3 else CERTFILE_CRT
KEYFILE_TLS = argv[4] if len(argv) > 4 else KEYFILE_TLS
CHAIN_PEM = argv[5] if len(argv) > 5 else CHAIN_PEM
# python3 GRPC/main_client.py fla-service-a.fla-na-a.svc 50051 './.certs-self/tls.crt' './.certs-self/tls.key' './.certs-self/chain.pem'


def run(user_name="John Doe", age=30, email="johndoe@example.com"):
    # set tls
    try:
        credentials = grpc.ssl_channel_credentials(open(CHAIN_PEM,'rb').read(), open(KEYFILE_TLS,'rb').read(), open(CERTFILE_CRT,'rb').read())
        channel = grpc.secure_channel(f'{GRPC_HOST}:{GRPC_PORT}', credentials)
        print(f'SSL_GRPC_INIT: {CHAIN_PEM} {KEYFILE_TLS} {CERTFILE_CRT}')
    except Exception as e:
        print(f'SSL_GRPC_ERROR_ELSE_NO_SSL: {e} {KEYFILE_TLS}')
        channel = grpc.insecure_channel(f'{GRPC_HOST}:{GRPC_PORT}')
    
    stub = userexample_pb2_grpc.UserExampleServiceStub(channel)

    # Ejemplo de creación de usuario
    user = userexample_pb2.User(user_name=user_name, age=age, email=email)

    # Ejemplo de obtención de usuario
    response = stub.GetUser(user)
    print("User getter:", response)


if __name__ == '__main__':
    run()