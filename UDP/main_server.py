# allow import from previous path
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import socket
import logging
from sys import argv

from application.utils import printing
from application.config import UDP_IP_ALLOW, UDP_PORT

logging.basicConfig(level=logging.DEBUG)

UDP_IP_ALLOW = argv[1] if len(argv) > 1 else UDP_IP_ALLOW
UDP_PORT = argv[2] if len(argv) > 2 else UDP_PORT
# python UDP/main_server.py '0.0.0.0' '5005'


printing(f'(print) UDP starting ... {UDP_PORT}')
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
        printing(message)
        logging.info(message)


if __name__ == "__main__":
    app(host=UDP_IP_ALLOW, port=int(UDP_PORT))
