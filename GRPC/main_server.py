import os
import grpc
from concurrent import futures
import time

from proto_grpc import userexample_pb2
from proto_grpc import userexample_pb2_grpc

WORKERS = os.getenv('WORKERS', '3')
GRPC_PORT = os.getenv('GRPC_PORT', '50051')


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
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()