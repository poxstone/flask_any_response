import os
import logging
import socket
import subprocess
from time import sleep
from flask import Flask, request, redirect, url_for


logging.basicConfig(level=logging.DEBUG)
application = app = Flask(__name__)
ENV = os.environ
FULL_METHODS = ['POST', 'GET', 'HEAD', 'PUT', 'DELETE']


def print_request(request, title="Response"):
    response = f'<h1>{title}</h1>'
    for i in dir(request):
      key = str(i)
      if not (key.startswith('_') or key.startswith('__')):
          response = ('{}\n<b>{}</b> = {}'.format(response, key, getattr(request, key)))
    
    message = '<pre>{}\n env = {}<pre>'.format(response,  ENV)
    logging.info(message)
    return message


def ping(host, count='3'):
    command = ['ping', '-c', count, host]
    return subprocess.call(command) == 0


def getPost(request):
    param = None
    try:
        param = request.form.to_dict()
        if len(param) == 0:
            raise Exception("no dict")
    except:
        param = request.json
    return param


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
    
    message = '<pre>UDP_IP = {}\n UDP_PORT = {}\n MESSAGE = {}<pre>'\
                .format(UDP_IP,  UDP_PORT, str(MESSAGE))
    logging.info(message)
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    server_address = (UDP_IP, int(UDP_PORT))
    sock.sendto(MESSAGE, server_address)
    
    return '{} ---- {}'.format(message, print_request(request, title="udp"))


@app.route('/', methods=FULL_METHODS)
def l0():
    return print_request(request)


@app.route('/ping/<host>/', methods=FULL_METHODS)
def doPing(host):
    count = request.args.get('count') if request.args.get('count') else '3'
    res = ping(host=host, count=count)
    return str(res)


@app.route('/bucketlist/<project>', methods=FULL_METHODS)
def bucketList(project):
    from googleapiclient.discovery import build
    from oauth2client.client import GoogleCredentials

    credentials = GoogleCredentials.get_application_default()
    service = build('storage', 'v1', credentials=credentials)
    response = service.buckets().list(project=project).execute()
    return str(response)


@app.route('/do/com/', methods=['POST'])
def doCom():
    command = getPost(request)
    if ('command' in command):
        res = str(subprocess.check_output(command['command']).decode("utf-8"))
        subprocess.check_output(['date'])
        sleep(1)
        logging.info('command: ' + res)
        return res
    return 'nothing to do'


@app.route('/requests/<protocol>/<domain>/<port>/', methods=FULL_METHODS)
def requests(protocol, domain, port):
    import requests
    method = request.args.get('method').upper() if request.args.get('method') \
                                                else request.method
    path = request.args.get('path') if request.args.get('path') else ''
    path = path if path.startswith('/') else '/{}'.format(path)
    parameters = ''
    search_path = request.full_path.rsplit('?')
    # build url search
    if len(search_path) > 1:
        for i in range(1, len(search_path)):
            parameters += '?{}'.format(search_path[i])
    body_data = {}
    if request.form:
        body_data = getPost(request)

    request.full_path
    url = '{protocol}://{domain}:{port}{path}{parameters}'.format(
                                                            protocol=protocol,
                                                            domain=domain,
                                                            port=port,
                                                            path=path,
                                                            parameters=parameters)
    res = ''
    if method == 'GET':
        res = requests.get(url).text
    elif method == 'POST':
        res = requests.post(url, data=body_data).text
    else:
        res = 'not supported method'
    return str(res)

@app.route('/redirect/relative', methods=FULL_METHODS)
def redirect_relative():
    return redirect(url_for('redirected'))


@app.route('/redirect/absolute/<protocol>/<domain>/<port>', methods=FULL_METHODS)
def redirect_absolute(protocol, domain, port):
    return redirect(f'{protocol}://{domain}:{port}/redirection/redirected')


@app.route('/redirect/redirected', methods=FULL_METHODS)
def redirected():
    return print_request(request, title="Redirected")

    
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
