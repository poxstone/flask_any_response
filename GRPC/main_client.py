import os
import grpc
from sys import argv

from proto_grpc import userexample_pb2
from proto_grpc import userexample_pb2_grpc

GRPC_HOST = argv[1] if len(argv[1]) > 1 else os.getenv('GRPC_HOST', '127.0.0.1')  # local.poxsilver5.store
GRPC_PORT = argv[2] if len(argv[2]) > 2 else os.getenv('GRPC_PORT', '50051')
CERTFILE_CRT = argv[3] if len(argv[3]) > 3 else os.getenv('CERTFILE_CRT', './.certs/tls.crt')
KEYFILE_TLS = argv[4] if len(argv[4]) > 4 else os.getenv('KEYFILE_TLS', './.certs/tls.key')
CA_CERT_TLS = argv[5] if len(argv[5]) > 5 else os.getenv('CA_CERT_TLS', './.certs/chain.pem')


def run(user_name="John Doe", age=30, email="johndoe@example.com"):
    # set tls
    try:
        credentials = grpc.ssl_channel_credentials(open(CA_CERT_TLS,'rb').read(), open(KEYFILE_TLS,'rb').read(), open(CERTFILE_CRT,'rb').read())
        channel = grpc.secure_channel(f'{GRPC_HOST}:{GRPC_PORT}', credentials)
    except Exception as e:
        print(f'SSL_ERROR_ELSE_NO_SSL: {e}')
        channel = grpc.insecure_channel(f'{GRPC_HOST}:{GRPC_PORT}')
    
    stub = userexample_pb2_grpc.UserExampleServiceStub(channel)

    # Ejemplo de creación de usuario
    user = userexample_pb2.User(user_name=user_name, age=age, email=email)

    # Ejemplo de obtención de usuario
    response = stub.GetUser(user)
    print("User getter:", response)


if __name__ == '__main__':
    run()