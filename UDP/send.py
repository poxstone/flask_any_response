import socket
import os

ENV = os.environ

UDP_IP = ENV["EXT_HOST"] if "EXT_HOST" in ENV else "127.0.0.1"
UDP_PORT = ENV['UDP_PORT'] if 'UDP_PORT' in ENV else 5005
MESSAGE = b"Hello, World!"


print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, int(UDP_PORT)))
