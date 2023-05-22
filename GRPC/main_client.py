import os
import grpc

from proto_grpc import userexample_pb2
from proto_grpc import userexample_pb2_grpc

GRPC_HOST = os.getenv('GRPC_HOST', '127.0.0.1')
GRPC_PORT = os.getenv('GRPC_PORT', '50051')


def run(user_name="John Doe", age=30, email="johndoe@example.com"):
    channel = grpc.insecure_channel(f'{GRPC_HOST}:{GRPC_PORT}')
    stub = userexample_pb2_grpc.UserExampleServiceStub(channel)

    # Ejemplo de creación de usuario
    user = userexample_pb2.User(user_name=user_name, age=age, email=email)

    # Ejemplo de obtención de usuario
    response = stub.GetUser(user)
    print("User getter:", response)


if __name__ == '__main__':
    run()