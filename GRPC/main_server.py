import os
import grpc
from sys import argv
from concurrent import futures
import time

from proto_grpc import userexample_pb2
from proto_grpc import userexample_pb2_grpc

CERTFILE_CRT = argv[1] if len(argv) > 1 else os.getenv('CERTFILE_CRT', './.certs/tls.crt')
KEYFILE_TLS = argv[2] if len(argv) > 2 else os.getenv('KEYFILE_TLS', './.certs/tls.key')
GRPC_PORT = argv[3] if len(argv) > 3 else os.getenv('GRPC_PORT', '50051')
WORKERS = os.getenv('WORKERS', '1')

# python3 GRPC/main_server.py './.certs-self/tls.crt' './.certs-self/tls.key' 50051


# curl example
class UserExampleServicer(userexample_pb2_grpc.UserExampleServiceServicer):
    def CreateUser(self, request, context):
        return userexample_pb2.User(user_name=request.user_name, age=request.age, email=request.email)

    def GetUser(self, request, context):
        return userexample_pb2.User(user_name=request.user_name, age=request.age, email=request.email)

    def UpdateUser(self, request, context):
        return userexample_pb2.User(user_name=request.user_name, age=request.age, email=request.email)

    def DeleteUser(self, request, context):
        return userexample_pb2.User(user_name=request.user_name, age=request.age, email=request.email)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(WORKERS)))
    userexample_pb2_grpc.add_UserExampleServiceServicer_to_server(UserExampleServicer(), server)
    # set tls
    try:
        server_credentials = grpc.ssl_server_credentials([( open(KEYFILE_TLS,'rb').read(), open(CERTFILE_CRT,'rb').read() )])
        server.add_secure_port(f'[::]:{GRPC_PORT}', server_credentials)
        print(f'SSL_GRPC_INIT: {KEYFILE_TLS} {CERTFILE_CRT}')
    except Exception as e:
        print(f'SSL_GRPC_ERROR_ELSE_NO_SSL: {e}')
        server.add_insecure_port(f'[::]:{GRPC_PORT}')

    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()