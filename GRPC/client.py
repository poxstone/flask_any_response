from __future__ import print_function

import os
import logging

import grpc
import hello_grpc

GRPC_PORT = os.getenv('GRPC_PORT', '50051')
GRPC_HOST = os.getenv('GRPC_HOST', '0.0.0.0')


def run():
    print("Will try to greet world ...")
    with grpc.insecure_channel(f'{GRPC_HOST}:{GRPC_PORT}') as channel:
        stub = hello_grpc.GreeterStub(channel)
        response = stub.SayHello(hello_grpc.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
