import os
import json
import logging
import socket
import datetime
import subprocess
import re
from time import sleep
from flask import Flask, request, redirect, url_for, Response
# email
import smtplib
import sys

logging.basicConfig(level=logging.DEBUG)
application = app = Flask(__name__)
ENV = os.environ
FULL_METHODS = ['POST', 'GET', 'HEAD', 'PUT', 'DELETE']
PATH_IGNORE = os.getenv('PATH_IGNORE', "favicon.ico,blank,echo.php,proxy.php")
VERSION_DEP = os.getenv('VERSION_DEP', 'nover')
GOOGLE_CLOUD_PROJECT = os.getenv('GOOGLE_CLOUD_PROJECT', '')

# gcp profiler
"""
try:
    logging.info(f'ERROR_vars_init: VERSION_DEP={VERSION_DEP} -- GOOGLE_CLOUD_PROJECT={GOOGLE_CLOUD_PROJECT}')
    import googlecloudprofiler
    if GOOGLE_CLOUD_PROJECT:
        googlecloudprofiler.start(service='flask_any_response', service_version=VERSION_DEP, verbose=3, project_id=GOOGLE_CLOUD_PROJECT )
    else:
        googlecloudprofiler.start(service='flask_any_response', service_version=VERSION_DEP, verbose=3)

except (ValueError, NotImplementedError) as exc:
    logging.info(f'ERROR_flaskanyresponse_profiler: {exc}')
"""


def print_request(request, title="Response"):
    internal_ip = 'none'
    free_mem = 'none'
    try:
        internal_ip = str(subprocess.check_output(["./script.sh", "ip address"]).decode("utf-8"))
    except Exception as e:
        print(e)
    try:
        free_mem = str(subprocess.check_output(["./script.sh", "free -h"]).decode("utf-8"))
    except Exception as e:
        print(e)
    mime_type = "text/html"
    if re.match('.', request.path):
        path_ext = re.split(r'\.', request.path)[-1] 
        if re.match(r'((png)|(jpe?g)|(ico)|(gif)|(bmp))$', path_ext):
            mime_type = f"image/{path_ext}"
        elif re.match(r'((html?)|(css)|(css)|(ics)|(txt))$', path_ext):
            mime_type = f"text/{path_ext}"
        elif re.match(r'((json)|(ogg)|(pdf)|(rtf)|(xml))$', path_ext):
            mime_type = f"application/{path_ext}"
        elif re.match(r'((js))$', path_ext):
            mime_type = f"text/javascript"
        elif re.match(r'((bin))$', path_ext):
            mime_type = f"application/octet-stream"
        else:
            mime_type = "text/html"

    response = f"""<h1>{title}</h1>
<small>date_system = {str(datetime.datetime.now())}</small>
<small>date_utc = {str(datetime.datetime.utcnow())}</small>
<small>mime_type = {str(mime_type)}</small>
<small>ip_address = {str(internal_ip)}</small>
<small>free_mem = {str(free_mem)}</small>dock
"""
    for i in dir(request):
        try:
            key = str(i)
            if not (key.startswith('_') or key.startswith('__')):
                response = ('{}\n<b>{}</b> = {}'.format(response, key, getattr(request, key)))
        except Exception as e:
            print(e)
    
    message = '<pre>{}\n env = {}<pre>'.format(response,  ENV)
    logging.info(message)
    return message, mime_type


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
        try:
            param = request.json
        except:
            param = {}
    return param


@app.route('/', methods=FULL_METHODS)
def l0():
    logging.info('lv0():')
    resp, mime_type = print_request(request, title='lv0():')
    return Response(resp, mimetype=mime_type)


@app.route('/testudp/', methods=FULL_METHODS)
def testudp():
    logging.info('testudp():')
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
    resp, mime_type = print_request(request, title="testudp():")
    return '{} ---- {}'.format(message, resp)


@app.route('/ping/<host>/', methods=FULL_METHODS)
def doPing(host):
    logging.info('doPing(host):')
    count = request.args.get('count') if request.args.get('count') else '3'
    res = ping(host=host, count=count)
    return str(res)

@app.route('/testsmtp/<host>/<email>/<pwd>', methods=FULL_METHODS)
def sendEmail(host, email, pwd):
    # Sending the mail
    try:
        server = smtplib.SMTP(host) # smtp.gmail.com:587
        server.starttls()
        server.login(email,pwd)
        server.quit()
        logging.info('command: ' + "loging")
        print("loging")
        return str("loging")
    except Exception as e:
        logging.info('command: ' + str(e))
        return str(e)


@app.route('/bucketlist/<project>', methods=FULL_METHODS)
def bucketList(project):
    logging.info('bucketList(project):')
    from googleapiclient.discovery import build
    from oauth2client.client import GoogleCredentials

    credentials = GoogleCredentials.get_application_default()
    service = build('storage', 'v1', credentials=credentials)
    response = service.buckets().list(project=project).execute()
    return str(response)


@app.route('/do/com/', methods=['POST'])
def doCom():
    logging.info('doCom():')
    command = getPost(request)
    if ('command' in command):
        res = str(subprocess.check_output(command['command']).decode("utf-8"))
        subprocess.check_output(['date'])
        sleep(1)
        logging.info('command: ' + res)
        return f"command: {command['command']} > response: \n {res}"
    return 'nothing to do'


@app.route('/do/script/', methods=['POST'])
def doScript():
    logging.info('doScript():')
    command = getPost(request)
    if ('command' in command):
        if type(command['command']) is not str:
            command['command'] = ' '.join(command['command'])
        logging.info('command_to_do: ' + command['command'])
        try:
            res = str(subprocess.check_output(["./script.sh", command['command']]).decode("utf-8"))
        except Exception as e:
            res = f'COMMAND_ERROR: {str(e)}'
        subprocess.check_output(['date'])
        logging.info('command: ' + res)
        return f"command: {command['command']} > response: \n {res}"
    return 'nothing to do'


@app.route('/requests/<protocol>/<domain>/<port>/', methods=FULL_METHODS)
def requests(protocol, domain, port):
    logging.info('requests(protocol, domain, port):')
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
    if method in ['POST','PUT','DELETE','PATCH'] and request.args.get('body'):
        try:
            body_data = json.loads(request.args.get('body'))
        except:
            body_data = {}
    else:
        body_data = getPost(request)
    
    if request.form:
        body_data = getPost(request)

    request.full_path
    url = f'{protocol}://{domain}:{port}{path}{parameters}'
    res = ''
    if method == 'GET':
        res = requests.get(url).text
    elif method == 'POST':
        res = requests.post(url, data=body_data).text
    elif method == 'DELETE':
        res = requests.delete(url, data=body_data).text
    elif method == 'PUT':
        res = requests.put(url, data=body_data).text
    elif method == 'PATCH':
        res = requests.patch(url, data=body_data).text
    else:
        res = 'not supported method'
    return str(res)


# relative dir
@app.route('/redirect/relative', methods=FULL_METHODS)
def redirect_relative():
    logging.info('redirect_relative():')
    return redirect(url_for('redirected'))


@app.route('/redirect/absolute/<protocol>/<domain>/<port>', methods=FULL_METHODS)
def redirect_absolute(protocol, domain, port):
    logging.info('redirect_absolute(protocol, domain, port):')
    path = request.args.get('path') if request.args.get('path') else ''
    path = path if path.startswith('/') else '/{}'.format(path)
    location = f'{protocol}://{domain}:{port}{path}'
    return redirect(location)


@app.route('/redirect/redirected', methods=FULL_METHODS)
def redirected():
    logging.info('redirected(): 302')
    resp, mime_type = print_request(request, title="Redirected")
    return Response(resp, mimetype=mime_type)

    
@app.route('/<lv1>', methods=FULL_METHODS)
def l1(lv1):
    if lv1 in PATH_IGNORE.split(','):
        return ""

    logging.info('def l1(lv1):')
    resp, mime_type = print_request(request)
    return Response(resp, mimetype=mime_type)


@app.route('/<lv1>/<lv2>', methods=FULL_METHODS)
def l2(lv1, lv2):
    logging.info('def l2(lv1, lv2):')
    resp, mime_type = print_request(request)
    return Response(resp, mimetype=mime_type)


@app.route('/<lv1>/<lv2>/<lv3>', methods=FULL_METHODS)
def l3(lv1, lv2, lv3):
    logging.info('def l3(lv1, lv2, lv3):')
    resp, mime_type = print_request(request)
    return Response(resp, mimetype=mime_type)


@app.route('/<lv1>/<lv2>/<lv3>/<lv4>', methods=FULL_METHODS)
def l4(lv1, lv2, lv3, lv4):
    logging.info('def l4(lv1, lv2, lv3, lv4):')
    resp, mime_type = print_request(request)
    return Response(resp, mimetype=mime_type)


@app.route('/<lv1>/<lv2>/<lv3>/<lv4>/<lv5>', methods=FULL_METHODS)
def lv5(lv1, lv2, lv3, lv4, lv5):
    logging.info('lv5(lv1, lv2, lv3, lv4, lv5):')
    resp, mime_type = print_request(request)
    return Response(resp, mimetype=mime_type)


@app.route('/<lv1>/<lv2>/<lv3>/<lv4>/<lv5>/<lv6>', methods=FULL_METHODS)
def lv6(lv1, lv2, lv3, lv4, lv5, lv6):
    logging.info('lv6(lv1, lv2, lv3, lv4, lv5, lv6):')
    resp, mime_type = print_request(request)
    return Response(resp, mimetype=mime_type)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="8080")


print("POXSTONE_LOG --- Flask Ended")