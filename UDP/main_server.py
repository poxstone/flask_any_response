import socket
import logging
import os
from sys import argv

logging.basicConfig(level=logging.DEBUG)

UDP_IP_ALLOW = argv[1] if len(argv) > 1 else os.getenv('UDP_IP_ALLOW', '0.0.0.0')
UDP_PORT = argv[2] if len(argv) > 2 else os.getenv('UDP_PORT', '5005')

# python UDP/main_server.py '0.0.0.0' '5005'


print(f'(print) UDP starting ... {UDP_PORT}')
logging.info(f'(logging.info) UDP starting ... {UDP_PORT}')


def app(host=UDP_IP_ALLOW, port=UDP_PORT):
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP_ALLOW, int(UDP_PORT)))
    
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        message = f'''RECEIVED MESSAGE: {str(data)}
                      ADDRESS: {str(addr)};
                      ENV: {str(os.environ)}'''
        print(message)
        logging.info(message)


if __name__ == "__main__":
    app(host=UDP_IP_ALLOW, port=int(UDP_PORT))
