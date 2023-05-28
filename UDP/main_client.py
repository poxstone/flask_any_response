import socket
import os
from sys import argv


UDP_IP = argv[1] if len(argv) > 1 else os.getenv('UDP_IP', '127.0.0.1')
UDP_PORT = argv[2] if len(argv) > 2 else os.getenv('UDP_PORT', '5005')
UDP_MESSAGE = argv[3] if len(argv) > 3 else os.getenv('UDP_MESSAGE', 'Hello, World!')

# python3 UDP/main_client.py 'fla-service-a.default-a.svc' '5005' 'Hello, World!'

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("UDP_message: %s" % UDP_MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(UDP_MESSAGE,'utf-8'), (UDP_IP, int(UDP_PORT)))
