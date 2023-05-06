import os
from concurrent import futures
import logging

import grpc
#import hello
import hello_grpc


GRPC_PORT = os.getenv('GRPC_PORT', '50051')
WORKERS = os.getenv('WORKERS', '1')

class Greeter(hello_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return hello_grpc.HelloReply(message='Hello, %s!' % request.name)


def serve():
    port = GRPC_PORT
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(WORKERS)))
    hello_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
