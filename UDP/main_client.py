# allow import from previous path
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import socket
from sys import argv

from application.utils import printing
from application.config import UDP_IP, UDP_PORT

UDP_IP = argv[1] if len(argv) > 1 else UDP_IP
UDP_PORT = argv[2] if len(argv) > 2 else UDP_PORT
UDP_MESSAGE = argv[3] if len(argv) > 3 else os.getenv('UDP_MESSAGE', 'Hello, World!')

# python3 UDP/main_client.py 'fla-service-a.default-a.svc' '5005' 'Hello, World!'

printing(f"UDP target IP: {UDP_IP}")
printing(f"UDP target port: {UDP_PORT}")
printing(f"UDP_message: {UDP_MESSAGE}")

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(UDP_MESSAGE,'utf-8'), (UDP_IP, int(UDP_PORT)))
