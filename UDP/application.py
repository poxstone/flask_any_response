import socket
import logging
import os

logging.basicConfig(level=logging.DEBUG)

ENV = os.environ
UDP_IP = "0.0.0.0"
UDP_PORT = ENV['UDP_PORT'] if 'UDP_PORT' in ENV else 5005

print("(print) UDP starting ... {}".format(UDP_PORT))
logging.info("(logging.info) UDP starting ... {}".format(UDP_PORT))


def app(host=UDP_IP, port=UDP_PORT):
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, int(UDP_PORT)))
    
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        message = "RECEIVED MESSAGE: {}; ADDRESS: {}; ENV: {}".format(
                                                str(data), str(addr), str(ENV))
        print(message)
        logging.info(message)


if __name__ == "__main__":
    app(host=UDP_IP, port=int(UDP_PORT))
