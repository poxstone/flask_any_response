import os
import json
import logging
import socket
import datetime
import subprocess
import asyncio
import functions_framework
from time import sleep
from application.config import *
from application.utils import get_random_string, printing, print_request, ping ,getPost ,do_request_method_async ,do_request_method, config_response
from flask import Flask, request, redirect, url_for, Response, render_template, send_file, make_response
# email
import smtplib


printing(f'INSTANCEID={STR_GLOBAL}')
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
    response, status_code = config_response(request, 'lv0():')
    return response, status_code


@app.route('/ping/<host>', methods=FULL_METHODS)
def doPing(host):
    printing('doPing(host):')
    count = request.args.get('count') if request.args.get('count') else '3'
    wait = request.args.get('wait') if request.args.get('wait') else '5'
    res = ping(host=host, count=count, wait=wait)
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


@app.route('/do/com', methods=['POST'])
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


@app.route('/do/script', methods=['POST'])
def doScript():
    printing('doScript():')
    command = getPost(request)
    if ('command' in command):
        if type(command['command']) is not str:
            command['command'] = ' '.join(command['command'])
        printing('command_to_do: ' + command['command'])
        try:
            res = str(subprocess.check_output(
                ["sh", "./script.sh", command['command']]).decode("utf-8"),
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
        except Exception as e:
            res = f'COMMAND_ERROR: {str(e)}'
        subprocess.check_output(['date'])
        printing('command: ' + res)
        return f"command: {command['command']} > response: \n {res}"
    return 'nothing to do', GLOBAL_STATE


@app.route('/requests/<protocol>/<domain>/<port>', methods=FULL_METHODS)
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


@app.route('/udp-requests/<domain>/<port>', methods=FULL_METHODS)
def testudp(domain, port):
    printing('testudp():')
    req_val = request.values

    UDP_IP = domain
    UDP_PORT = port
    MESSAGE = bytes(req_val.get('MESSAGE'), 'utf-8') if req_val.get('MESSAGE') else bytes(UDP_MESSAGE, 'utf-8')

    message = '<pre>UDP_IP = {}\n UDP_PORT = {}\n MESSAGE = {}<pre>'\
                .format(UDP_IP,  UDP_PORT, str(MESSAGE))
    printing(message)
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    server_address = (UDP_IP, int(UDP_PORT))
    sock.sendto(MESSAGE, server_address)
    resp, mime_type, status_code, message_code = print_request(request, title="testudp():")
    return '{} ---- {}'.format(message, resp), status_code


@app.route('/grpc-requests/<domain>/<port>', methods=FULL_METHODS)
def grpc_requests(domain, port):
    printing('grpc_requests(domain, port):')
    resp, mime_type, status_code, message_code = print_request(request, title='grpc_requests(domain, port):', print_logs='false')
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
        printing(f'SSL_ERROR_ELSE_NO_SSL: {e}')
        channel = grpc.insecure_channel(f'{domain}:{port}')

    stub = userexample_pb2_grpc.UserExampleServiceStub(channel)
    # create grpc
    user = userexample_pb2.User(user_name=body_data['user_name'], age=int(body_data['age']), email=body_data['email'])
    # Get response grpc
    response = stub.GetUser(user)
    printing(f"User getter: {str(response)}")

    return f"Greeter client received: {str(response)}", status_code


@app.route('/concat-requests/<num>', methods=FULL_METHODS)
def concat_requests(num):
    printing(f'/concat-requests/{num}/')
    import requests
    hosts = request.args.get('hosts').lower() if request.args.get('hosts') else ''
    printing('concat_requests num={num} - hosts={hosts}:')
    if not hosts:
        resp, mime_type, status_code, message_code = print_request(request)
        return Response(resp, mimetype=mime_type), status_code

    path = hosts.split(',')[0]
    hosts_query = f'?hosts={",".join(hosts.split(",")[1:])}'
    url = f'{hosts.split(",")[0]}/concat-requests/{int(num)+1}/{hosts_query}'
    
    res = requests.get(url).text
    return str(res), GLOBAL_STATE


@app.route('/json-requests/<num>', methods=FULL_METHODS)
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


# test socket
@app.route('/socket-requests/<protocol>/<domain>/<port>/<path>')
def socket_request(protocol, domain, port, path):
    resp, mime_type, status_code, message_code = print_request(request, title="Redirected")
    return render_template('socket-requests-client.html'), status_code


# relative dir
@app.route('/redirect-relative', methods=FULL_METHODS)
def redirect_relative():
    printing('redirect_relative():')
    return redirect(url_for('redirected'))


@app.route('/redirect-absolute/<protocol>/<domain>/<port>', methods=FULL_METHODS)
def redirect_absolute(protocol, domain, port):
    printing('redirect_absolute(protocol, domain, port):')
    path = request.args.get('path') if request.args.get('path') else ''
    path = path if path.startswith('/') else '/{}'.format(path)
    location = f'{protocol}://{domain}:{port}{path}'
    return redirect(location)


@app.route('/redirect-redirected', methods=FULL_METHODS)
def redirected():
    response, status_code = config_response(request, 'redirected(): 302')
    return response, status_code


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
    # ignore favicon.ico
    if lv1 in PATH_IGNORE.split(','):
        return ""
    response, status_code = config_response(request, 'def l1(lv1):')
    return response, status_code


@app.route('/<lv1>/<lv2>', methods=FULL_METHODS)
def l2(lv1, lv2):
    response, status_code = config_response(request, 'def l2(lv1, lv2):')
    return response, status_code


@app.route('/<lv1>/<lv2>/<lv3>', methods=FULL_METHODS)
def l3(lv1, lv2, lv3):
    response, status_code = config_response(request, 'def l3(lv1, lv2, lv3):')
    return response, status_code


@app.route('/<lv1>/<lv2>/<lv3>/<lv4>', methods=FULL_METHODS)
def l4(lv1, lv2, lv3, lv4):
    response, status_code = config_response(request, 'def l4(lv1, lv2, lv3, lv4):')
    return response, status_code


@app.route('/<lv1>/<lv2>/<lv3>/<lv4>/<lv5>', methods=FULL_METHODS)
def lv5(lv1, lv2, lv3, lv4, lv5):
    response, status_code = config_response(request, 'lv5(lv1, lv2, lv3, lv4, lv5):')
    return response, status_code


@app.route('/<lv1>/<lv2>/<lv3>/<lv4>/<lv5>/<lv6>', methods=FULL_METHODS)
def lv6(lv1, lv2, lv3, lv4, lv5, lv6):
    response, status_code = config_response(request, 'lv6(lv1, lv2, lv3, lv4, lv5, lv6):')
    return response, status_code


@app.route('/<lv1>/<lv2>/<lv3>/<lv4>/<lv5>/<lv6>', methods=FULL_METHODS)
def lv7(lv1, lv2, lv3, lv4, lv5, lv6, lv7):
    response, status_code = config_response(request, 'lv6(lv1, lv2, lv3, lv4, lv5, lv6, lv7):')
    return response, status_code


@app.route('/google-dfcx/<go>', methods=FULL_METHODS)
def dialogflow_reply(go):
    printing(f'/dfcx/<go>')
    return dialogflow_trigger(request)


@functions_framework.http
def dialogflow_trigger(request):
    response, status_code = config_response(request, 'dialogflow_response')
    request_json = request.get_json(silent=True)

    if not request_json:
        printing("Error: No se recibió un cuerpo JSON válido.")
        request_json = {}

    tag = request_json.get("fulfillmentInfo", {}).get("tag")
    intent_name = request_json.get("intentInfo", {}).get("displayName")
    session_params = request_json.get("sessionInfo", {}).get("parameters", {})
    
    response_text = ""
    if tag == "saludo_webhook":
        response_text = f"Hola desde el webhook! Recibí la intención '{intent_name}'."
    elif tag == "consultar_producto":
        producto_id = session_params.get("producto_id", "ninguno")
        response_text = f"Consultando información para el producto: {producto_id}."
    else:
        response_text = f"Webhook contactado, pero no se encontró una acción para este tag. '{intent_name}'"

    response_payload = {
        "fulfillment_response": {"messages": [
            {"text": {
                "text": [response_text],
                "allow_playback_interruption": False
            }}]}}
    printing(response_payload)
    return json.dumps(response_payload), 200, {'Content-Type': 'application/json'}


@app.route('/gcf/<go>', methods=FULL_METHODS)
def functions_reply(go):
    response, status_code = config_response(request, '/gcf/<go>')
    return functions_trigger(request)


@functions_framework.http
def functions_trigger(request):
    response, status_code = config_response(request, 'functions_trigger', print_logs='true')

    # reenvia la solicitud a curl
    if request.path.startswith('/requests/'):
        parts = request.path.strip('/').split('/')
        if len(parts) >= 4:
            protocol, domain, port = parts[1], parts[2], parts[3]
            return requests(protocol, domain, port)

    # valida un permisos de buckets
    if request.path == '/gcf/gcs-test' and os.environ.get('SERVICE') == 'gcs-test':
        request_json = request.get_json(silent=True)
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "project-not-found")
        return bucketList(project_id)

    return response


@functions_framework.http
def azure_bot_trigger(request):
    import asyncio
    from botbuilder.schema import Activity
    from application.azure_bot import DialogflowBot
    from application.service_dialog_flow_cx import detect_intent_text, extract_text_from_dialogflow_response

    response, status_code = config_response(request, 'azure_bot_trigger')
    try:
        body = request.json
        ms_bot_tenant_id = body['conversation']['tenantId']
        ms_bot_session_id = body['conversation']['id']
        ms_bot_from = body['from']
        ms_bot_text = body['text']
        ms_bot_language = body['locale']
        ms_bot_auth_header_x = request.headers.get("X-Forwarded-Authorization")  # for google api gateway
        ms_bot_auth_header = ms_bot_auth_header_x if ms_bot_auth_header_x else request.headers.get("Authorization")
        bot_connection = SECRETS_MS_TEAMS
        response_agent_text = f'{bot_connection["TEAMS_AUTO_RESPONSE"]}:: (ms_bot_text: {ms_bot_text}) - (ms_bot_tenant_id: {ms_bot_tenant_id})) - (ms_bot_session_id: {ms_bot_session_id}) -- (ms_bot_from: {ms_bot_from})'

        # get response from dialogflow
        try:
            response_dialog_agent = detect_intent_text(GOOGLE_CLOUD_PROJECT, LOCATION, bot_connection['GCP_DIALOGF_AGENT_ID'], ms_bot_session_id, ms_bot_text, ms_bot_language)
            response_agent_text = extract_text_from_dialogflow_response(response_dialog_agent)
        except Exception as e:
            printing(f"Error al obtener la respuesta de Dialogflow: {e}")

        activity = Activity().deserialize(body)
        bot_az_cli = DialogflowBot(bot_connection['TEAMS_APP_ID'], bot_connection['TEAMS_APP_ID'], 
                                  bot_connection['TEAMS_APP_PASSWORD'], bot_connection['TEAMS_TENANT_ID'],  response=response_agent_text)
        async def process_activity():
            await bot_az_cli.adapter.process_activity(activity, ms_bot_auth_header,
                                                      bot_az_cli.on_turn)
        asyncio.run(process_activity())
        # return response
        return Response(status=201)
    except Exception as e:
        printing(f"Error al procesar la actividad: {e}")
        return Response(status=500)


@app.route('/azure-bot/<go>', methods=FULL_METHODS)
def azure_bot_reply(go):
    response, status_code = config_response(request, '/azure-bot/<go>')
    return azure_bot_trigger(request)


printing(f'INIT_TIME_APP_PY_={STR_GLOBAL}: {str(datetime.datetime.now())}')

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=PORT)


printing(f"POXSTONE_LOG={STR_GLOBAL}: --- Flask Ended")

# gunicorn --workers="1" --timeout="120" --bind="0.0.0.0:8080" --certfile=".certs-self/tls.crt" --keyfile=".certs-self/tls.key" main:app;
# curl https://fla-service-a.fla-na-a.svc:8080 --cacert .certs-self/chain.pem