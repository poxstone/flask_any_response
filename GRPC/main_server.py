import os
import grpc
from concurrent import futures
import time

from proto_grpc import userexample_pb2
from proto_grpc import userexample_pb2_grpc

WORKERS = os.getenv('WORKERS', '3')
GRPC_PORT = os.getenv('GRPC_PORT', '50051')
CERTFILE_CRT = os.getenv('CERTFILE_CRT', './.certs/tls.crt')
KEYFILE_TLS = os.getenv('KEYFILE_TLS', './.certs/tls.key')

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
    except Exception as e:
        print(f'SSL_ERROR_ELSE_NO_SSL: {e}')
        server.add_insecure_port(f'[::]:{GRPC_PORT}')

    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()