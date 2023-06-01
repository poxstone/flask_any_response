import os
import json
import logging
import socket
import datetime
import subprocess
import asyncio
from time import sleep
from application.config import ENV, FULL_METHODS, PATH_IGNORE, REQUEST_STR_LENGTH, SLEEP_TIME, PORT, LOGS_PRINT, lets_token, CERTFILE_CRT, KEYFILE_TLS, CHAIN_PEM, STR_GLOBAL, GLOBAL_STATE
from application.utils import get_random_string, printing, print_request, ping ,getPost ,do_request_method_async ,do_request_method
from flask import Flask, request, redirect, url_for, Response, render_template, send_file
# email
import smtplib


print(f'INSTANCEID={STR_GLOBAL}')
logging.basicConfig(level=logging.DEBUG)
application = app = Flask(__name__, template_folder=os.path.abspath('htmls'))


# gcp profiler
"""
try:
    printing(f'ERROR_vars_init: VERSION_DEP={VERSION_DEP} -- GOOGLE_CLOUD_PROJECT={GOOGLE_CLOUD_PROJECT}')
    import googlecloudprofiler
    if GOOGLE_CLOUD_PROJECT:
        googlecloudprofiler.start(service='flask_any_response', service_version=VERSION_DEP, verbose=3, project_id=GOOGLE_CLOUD_PROJECT )
    else:
        googlecloudprofiler.start(service='flask_any_response', service_version=VERSION_DEP, verbose=3)

except (ValueError, NotImplementedError) as exc:
    printing(f'ERROR_flaskanyresponse_profiler: {exc}')
"""

@app.route('/', methods=FULL_METHODS)
def l0():
    printing('lv0():')
    resp, mime_type, status_code = print_request(request, title='lv0():')
    return Response(resp, mimetype=mime_type), status_code


@app.route('/testudp/', methods=FULL_METHODS)
def testudp():
    printing('testudp():')
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
    printing(message)
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    server_address = (UDP_IP, int(UDP_PORT))
    sock.sendto(MESSAGE, server_address)
    resp, mime_type, status_code = print_request(request, title="testudp():")
    return '{} ---- {}'.format(message, resp), status_code


@app.route('/ping/<host>/', methods=FULL_METHODS)
def doPing(host):
    printing('doPing(host):')
    count = request.args.get('count') if request.args.get('count') else '3'
    res = ping(host=host, count=count)
    return str(res), GLOBAL_STATE

@app.route('/testsmtp/<host>/<email>/<pwd>', methods=FULL_METHODS)
def sendEmail(host, email, pwd):
    # Sending the mail
    try:
        server = smtplib.SMTP(host) # smtp.gmail.com:587
        server.starttls()
        server.login(email,pwd)
        server.quit()
        printing('command: ' + "loging")
        printing("loging")
        return str("loging"), GLOBAL_STATE
    except Exception as e:
        printing('command: ' + str(e))
        return str(e), GLOBAL_STATE


@app.route('/bucketlist/<project>', methods=FULL_METHODS)
def bucketList(project):
    printing('bucketList(project):')
    from googleapiclient.discovery import build
    from oauth2client.client import GoogleCredentials

    credentials = GoogleCredentials.get_application_default()
    service = build('storage', 'v1', credentials=credentials)
    response = service.buckets().list(project=project).execute()
    return str(response), GLOBAL_STATE


@app.route('/do/com/', methods=['POST'])
def doCom():
    printing('doCom():')
    command = getPost(request)
    if ('command' in command):
        res = str(subprocess.check_output(command['command']).decode("utf-8"))
        subprocess.check_output(['date'])
        sleep(1)
        printing('command: ' + res)
        return f"command: {command['command']} > response: \n {res}"
    return 'nothing to do', GLOBAL_STATE


@app.route('/do/script/', methods=['POST'])
def doScript():
    printing('doScript():')
    command = getPost(request)
    if ('command' in command):
        if type(command['command']) is not str:
            command['command'] = ' '.join(command['command'])
        printing('command_to_do: ' + command['command'])
        try:
            res = str(subprocess.check_output(["./script.sh", command['command']]).decode("utf-8"))
        except Exception as e:
            res = f'COMMAND_ERROR: {str(e)}'
        subprocess.check_output(['date'])
        printing('command: ' + res)
        return f"command: {command['command']} > response: \n {res}"
    return 'nothing to do', GLOBAL_STATE


@app.route('/grpc-requests/<domain>/<port>/', methods=FULL_METHODS)
def grpc_requests(domain, port):
    printing('grpc_requests(domain, port):')
    resp, mime_type, status_code = print_request(request, title='grpc_requests(domain, port):', print_logs='false')
    import grpc
    #import GRPC.hello_grpc as hello_grpc
    from GRPC.proto_grpc import userexample_pb2
    from GRPC.proto_grpc import userexample_pb2_grpc

    body_data = {
        'user_name': 'John Doe',
        'age': '42',
        'email': 'John_doe@mail.com',
    }
    method = request.args.get('method').upper() if request.args.get('method') \
                                                else request.method
    
    if method in ['POST','PUT','DELETE','PATCH'] and request.args.get('body'):
        try:
            body_data = json.loads(request.args.get('body'))
        except:
            body_data = body_data
    else:
        if request.form:
            body_data = getPost(request)
        body_data = getPost(request) if getPost(request) else body_data
        
    path = request.args.get('path') if request.args.get('path') else ''
    path = path if path.startswith('/') else '/{}'.format(path)

    printing(f'TRY_GRPC to {domain}:{port}')

    channel = grpc.insecure_channel(f'{domain}:{port}')
    try:
        credentials = grpc.ssl_channel_credentials(open(CHAIN_PEM,'rb').read(), open(KEYFILE_TLS,'rb').read(), open(CERTFILE_CRT,'rb').read())
        channel = grpc.secure_channel(f'{domain}:{port}', credentials)
    except Exception as e:
        print(f'SSL_ERROR_ELSE_NO_SSL: {e}')
        channel = grpc.insecure_channel(f'{domain}:{port}')

    stub = userexample_pb2_grpc.UserExampleServiceStub(channel)
    # create grpc
    user = userexample_pb2.User(user_name=body_data['user_name'], age=int(body_data['age']), email=body_data['email'])
    # Get response grpc
    response = stub.GetUser(user)
    printing(f"User getter: {str(response)}")

    return f"Greeter client received: {str(response)}", status_code


@app.route('/requests/<protocol>/<domain>/<port>/', methods=FULL_METHODS)
def requests(protocol, domain, port):
    printing('requests(protocol, domain, port):')
    import requests
    method = request.args.get('method').upper() if request.args.get('method') \
                                                else request.method
    path = request.args.get('path') if request.args.get('path') else ''
    path = path if path.startswith('/') else '/{}'.format(path)
    headers_data = {}
    params_data = ''

    # get header
    if request.args.get('headers'):
        try:
            headers_data = json.loads(request.args.get('headers'))
        except:
            headers_data = {}

    # get search parameters
    if request.args.get('params'):
        try:
            params_data = '?' + request.args.get('params').replace(',','&')
        except:
            params_data = ''
    
    # get body
    if method in ['POST','PUT','DELETE','PATCH'] and request.args.get('body'):
        try:
            body_data = json.loads(request.args.get('body'))
        except:
            body_data = {}
    else:
        body_data = getPost(request)
    
    if request.form:
        body_data = getPost(request)
    
    url = f'{protocol}://{domain}:{port}{path}{params_data}'
    
    res = do_request_method(method, url, headers_data, body_data)
    return str(res), GLOBAL_STATE


@app.route('/concat-requests/<num>/', methods=FULL_METHODS)
def concat_requests(num):
    printing(f'/concat-requests/{num}/')
    import requests
    hosts = request.args.get('hosts').lower() if request.args.get('hosts') else ''
    printing('concat_requests num={num} - hosts={hosts}:')
    if not hosts:
        resp, mime_type, status_code = print_request(request)
        return Response(resp, mimetype=mime_type), status_code

    path = hosts.split(',')[0]
    hosts_query = f'?hosts={",".join(hosts.split(",")[1:])}'
    url = f'{hosts.split(",")[0]}/concat-requests/{int(num)+1}/{hosts_query}'
    
    res = requests.get(url).text
    return str(res), GLOBAL_STATE


@app.route('/json-requests/<num>/', methods=FULL_METHODS)
def json_requests(num):
    printing(f'json_requests')
    # get body
    req = ''
    body_data = {}
    try:
        body_data = getPost(request)
    except:
        return str(f'No body detected (GET not supported) {request}')

    request_full = body_data['body_data'] if 'body_data' in body_data else []
    res = []
    for requested in request_full:
        method = requested['method'] if 'method' in requested else 'GET'
        url = requested['url'] if 'url' in requested else f'http://localhost:{PORT}/'
        headers = requested['headers'] if 'headers' in requested else {}
        body = requested['body'] if 'body' in requested else {}
        if 'async' in requested and requested['async'] == 'true':
            #req = str(do_request_method_async(method, url, headers, body))
            #loop = asyncio.get_event_loop()
            task = asyncio.run(do_request_method_async(method, url, headers, body))
            #task = loop.create_task(do_request_method_async(method, url, headers, body))
            #loop.run_until_complete(task)
            #loop.close()
        else:
            req = do_request_method(method, url, headers, body)
        res.append(req)

    return str(res), GLOBAL_STATE


# relative dir
@app.route('/redirect/relative', methods=FULL_METHODS)
def redirect_relative():
    printing('redirect_relative():')
    return redirect(url_for('redirected'))


@app.route('/redirect/absolute/<protocol>/<domain>/<port>', methods=FULL_METHODS)
def redirect_absolute(protocol, domain, port):
    printing('redirect_absolute(protocol, domain, port):')
    path = request.args.get('path') if request.args.get('path') else ''
    path = path if path.startswith('/') else '/{}'.format(path)
    location = f'{protocol}://{domain}:{port}{path}'
    return redirect(location)


@app.route('/redirect/redirected', methods=FULL_METHODS)
def redirected():
    printing('redirected(): 302')
    resp, mime_type, status_code = print_request(request, title="Redirected")
    return Response(resp, mimetype=mime_type), status_code


# test socket
@app.route('/web-socket.html')
def index():
    return render_template('web-socket.html'), status_code


@app.route('/download/<size>')
def downloadFile (size):
    str_request = f'{STR_GLOBAL}-{get_random_string(int(REQUEST_STR_LENGTH))}'
    file_prefix = 'filedowload'
    file_name = f"{file_prefix}_{size}-{str_request}.bin"
    printing(f'{str_request}: - downloadFile({file_name}): generating...')
    try:
        # remover previously files
        res = str(subprocess.check_output(["./script.sh", f"rm -rf {file_prefix}*"]).decode("utf-8"))
        # generate file 1M 1G...
        res = str(subprocess.check_output(["./script.sh", f"fallocate -l {size} {file_name}"]).decode("utf-8"))
    except Exception as e:
        res = f'{str_request}: - COMMAND_ERROR: {str(e)}'
    path = f"{file_name}"
    printing(f'{str_request}: - Downloading...')
    return send_file(path, as_attachment=True)


# Lets encrypt
@app.route('/.well-known/acme-challenge/<hash2>', methods=FULL_METHODS)
def lets_encrypt(hash2):
    #lets_token = "vBvxn5Lcwets4GsiBhnvzlpXz8O3Fw1F6pIeCnheJWU.8nbTZcTXCOMNdGffVilLuytrq7uDN8SOAMGubsIm1II"
    printing(f'lets_encrypt(): {lets_token}')
    return lets_token.strip()

@app.route('/.well-known/acme-challenge/set/<hash1>', methods=FULL_METHODS)
def sets_encrypt(hash1):
    global lets_token
    lets_token = hash1.strip()
    printing(f'set_encrypt(): {lets_token}')
    return lets_token.strip()


@app.route('/set/status_code/<num>', methods=FULL_METHODS)
def sets_status_code(num):
    global GLOBAL_STATE
    GLOBAL_STATE = int(num)
    printing(f'set_status_code(): {GLOBAL_STATE}')
    return f'set_status_code(): {GLOBAL_STATE}', GLOBAL_STATE
    

@app.route('/<lv1>', methods=FULL_METHODS)
def l1(lv1):
    if lv1 in PATH_IGNORE.split(','):
        return ""

    printing('def l1(lv1):')
    resp, mime_type, status_code = print_request(request)
    return Response(resp, mimetype=mime_type), status_code


@app.route('/<lv1>/<lv2>', methods=FULL_METHODS)
def l2(lv1, lv2):
    printing('def l2(lv1, lv2):')
    resp, mime_type, status_code = print_request(request)
    return Response(resp, mimetype=mime_type), status_code


@app.route('/<lv1>/<lv2>/<lv3>', methods=FULL_METHODS)
def l3(lv1, lv2, lv3):
    printing('def l3(lv1, lv2, lv3):')
    resp, mime_type, status_code = print_request(request)
    return Response(resp, mimetype=mime_type), status_code


@app.route('/<lv1>/<lv2>/<lv3>/<lv4>', methods=FULL_METHODS)
def l4(lv1, lv2, lv3, lv4):
    printing('def l4(lv1, lv2, lv3, lv4):')
    resp, mime_type, status_code = print_request(request)
    return Response(resp, mimetype=mime_type), status_code


@app.route('/<lv1>/<lv2>/<lv3>/<lv4>/<lv5>', methods=FULL_METHODS)
def lv5(lv1, lv2, lv3, lv4, lv5):
    printing('lv5(lv1, lv2, lv3, lv4, lv5):')
    resp, mime_type, status_code = print_request(request)
    return Response(resp, mimetype=mime_type), status_code


@app.route('/<lv1>/<lv2>/<lv3>/<lv4>/<lv5>/<lv6>', methods=FULL_METHODS)
def lv6(lv1, lv2, lv3, lv4, lv5, lv6):
    printing('lv6(lv1, lv2, lv3, lv4, lv5, lv6):')
    resp, mime_type, status_code = print_request(request)
    return Response(resp, mimetype=mime_type), status_code


@app.route('/<lv1>/<lv2>/<lv3>/<lv4>/<lv5>/<lv6>', methods=FULL_METHODS)
def lv7(lv1, lv2, lv3, lv4, lv5, lv6, lv7):
    printing('lv6(lv1, lv2, lv3, lv4, lv5, lv6, lv7):')
    resp, mime_type, status_code = print_request(request)
    return Response(resp, mimetype=mime_type), status_code


print(f'INIT_TIME_APP_PY_={STR_GLOBAL}: {str(datetime.datetime.now())}')

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=PORT)


print(f"POXSTONE_LOG={STR_GLOBAL}: --- Flask Ended")

# gunicorn --workers="1" --timeout="120" --bind="0.0.0.0:8080" --certfile=".certs-self/tls.crt" --keyfile=".certs-self/tls.key" main:app;
# curl https://fla-service-a.default-a.svc:8080 --cacert .certs-self/chain.pem