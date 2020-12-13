import os
import logging
import socket
from flask import Flask, request


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
ENV = os.environ
FULL_METHODS = ['POST', 'GET', 'HEAD', 'PUT', 'DELETE']


def print_request(request):
    response = ''
    for i in dir(request):
      key = str(i)
      if not (key.startswith('_') or key.startswith('__')):
          response = ('{}\n<b>{}</b> = {}'.format(response, key, getattr(request, key)))
    
    message = '<pre>{}\n env = {}<pre>'.format(response,  ENV)
    logging.info(message)
    return message

@app.route('/testudp/', methods=FULL_METHODS)
def testudp():
    req_val = request.values
    try:
        UDP_IP = req_val.get('UDP_IP')
        UDP_PORT = req_val.get('UDP_PORT')
        MESSAGE = bytes(req_val.get('MESSAGE'), 'utf-8')
    except Exception as e:
        UDP_IP = ENV["UDP_IP"] if "UDP_IP" in ENV else "127.0.0.1"
        UDP_PORT = ENV['UDP_PORT'] if 'UDP_PORT' in ENV else 5005
        MESSAGE = b"Hello, World!"
    
    message = '<pre>{}\n UDP_IP = {}\n UDP_PORT = {}\n MESSAGE = MESSAGE<pre>'\
                .format(UDP_IP,  UDP_PORT, str(MESSAGE))
    logging.info(message)
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, int(UDP_PORT)))
    
    return print_request(message)


@app.route('/', methods=FULL_METHODS)
def l0():
    return print_request(request)

@app.route('/<lv1>', methods=FULL_METHODS)
def l1(lv1):
    return print_request(request)

@app.route('/<lv1>/<lv2>', methods=FULL_METHODS)
def l2(lv1, lv2):
    return print_request(request)

@app.route('/<lv1>/<lv2>/<lv3>', methods=FULL_METHODS)
def l3(lv1, lv2, lv3):
    return print_request(request)

@app.route('/<lv1>/<lv2>/<lv3>/<lv4>', methods=FULL_METHODS)
def l4(lv1, lv2, lv3, lv4):
    return print_request(request)

@app.route('/<lv1>/<lv2>/<lv3>/<lv4>/<lv5>', methods=FULL_METHODS)
def lv5(lv1, lv2, lv3, lv4, lv5):
    return print_request(request)

@app.route('/<lv1>/<lv2>/<lv3>/<lv4>/<lv5>/<lv6>', methods=FULL_METHODS)
def lv6(lv1, lv2, lv3, lv4, lv5, lv6):
    return print_request(request)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")
