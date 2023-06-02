# allow import from previous path
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import grpc
from sys import argv
from concurrent import futures
import time

from proto_grpc import userexample_pb2
from proto_grpc import userexample_pb2_grpc

from application.config import CERTFILE_CRT, KEYFILE_TLS, GRPC_PORT, WORKERS


CERTFILE_CRT = argv[1] if len(argv) > 1 else CERTFILE_CRT
KEYFILE_TLS = argv[2] if len(argv) > 2 else KEYFILE_TLS
GRPC_PORT = argv[3] if len(argv) > 3 else GRPC_PORT
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