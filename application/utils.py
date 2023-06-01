import random
import string
import datetime
import subprocess
import json
import re
from time import sleep
from .config import ENV, REQUEST_STR_LENGTH, SLEEP_TIME, LOGS_PRINT, STR_GLOBAL, GLOBAL_STATE


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def printing(string, print_logs='true'):
    if LOGS_PRINT.lower() == 'true':
        if print_logs == 'true':
            #logging.info(str(string))
            print(f'{str(string)} - time_back({STR_GLOBAL}):{str(datetime.datetime.now())}')
    return ''


def print_request(request, title="Response", print_logs='true'):
    str_request = f'{STR_GLOBAL}-{get_random_string(int(REQUEST_STR_LENGTH))}'
    internal_ip = 'none'
    free_mem = 'none'
    try:
        internal_ip = str(subprocess.check_output(["./script.sh", "ip address"]).decode("utf-8"))
    except Exception as e:
        printing(e)
    try:
        free_mem = str(subprocess.check_output(["./script.sh", "free -h"]).decode("utf-8"))
    except Exception as e:
        printing(e)
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
            printing(e)
    # trigger sleeptime
    try:
        sleep_time = float(request.args.get('sleep'))
        printing(f'{str_request}: - SLEEPING_FROM_GET({sleep_time})...')
        sleep(sleep_time)
    except:
        printing(f'{str_request}: - SLEEPING_FROM_ENV({SLEEP_TIME})...')
        sleep(float(SLEEP_TIME))
        pass
    # get status code
    try:
        status_code = int(request.args.get('status'))
    except:
        status_code = int(GLOBAL_STATE)
    message = '<pre>{}\n env = {}<pre>'.format(response,  ENV)
    message_code = ''
    for line in message.splitlines():
        message_code += f'{str_request}: {line}\n'
    printing(message_code, print_logs)
    return message_code, mime_type, status_code


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


async def do_request_method_async(method, url, headers_data, body_data):
    return do_request_method(method, url, headers_data, body_data)

def do_request_method(method, url, headers_data, body_data):
    import requests
    res = ''
    try:
        json_data = json.dumps(body_data)
    except Exception as e:
        json_data = '{}'
    try:
        if method == 'GET':
            res = requests.get(url, headers=headers_data).text
        elif method == 'POST':
            res = requests.post(url, data=json_data, headers=headers_data).text
        elif method == 'DELETE':
            res = requests.delete(url, data=json_data, headers=headers_data).text
        elif method == 'PUT':
            res = requests.put(url, data=json_data, headers=headers_data).text
        elif method == 'PATCH':
            res = requests.patch(url, data=json_data, headers=headers_data).text
        else:
            res = 'not supported method'
    except Exception as e:
        res = f'fail for: method:{method}, url:{url}, headers_data:{headers_data}, body_data:{body_data}'
    
    return str(res)
