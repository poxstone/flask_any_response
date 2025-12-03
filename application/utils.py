import random
import platform
import string
import datetime
import subprocess
import logging
import json
import re
from time import sleep
from .config import ENV, REQUEST_STR_LENGTH, SLEEP_TIME, LOGS_PRINT, STR_GLOBAL, GLOBAL_STATE, VIEW_PRINT, COOKIE_VAL, MAX_TIMEOUT
from flask import Response

logging.basicConfig(level=logging.DEBUG)

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def printing(string, print_logs='true'):
    if LOGS_PRINT.lower() == 'true':
        if print_logs == 'true' or print_logs is None:
            logging.info(f'_{str(string)} - time_back({STR_GLOBAL}):{str(datetime.datetime.now())}')
            print(f'{str(string)} - time_back({STR_GLOBAL}):{str(datetime.datetime.now())}')
    return ''


def print_request(request, title="Response", print_logs='true'):
    str_request = f'{STR_GLOBAL}-{get_random_string(int(REQUEST_STR_LENGTH))}'
    internal_ip = 'none'
    free_mem = 'none'
    response = ''
    message = ''
    message_code = ''
        # get status code
    try:
        status_code = int(request.args.get('status'))
    except:
        status_code = int(GLOBAL_STATE)
    # logs backend
    try:
        print_logs = request.args.get('print_logs')
    except:
        print_logs = print_logs if print_logs else LOGS_PRINT
    # print front
    try:
        view_print = request.args.get('view') if request.args.get('view') else VIEW_PRINT
    except:
        view_print = print_logs if print_logs else VIEW_PRINT
    
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
    if view_print == 'simple' or view_print == 'full':
        response = f"""<h1>{title}</h1>"""
        response += f"""<small>date_system = {str(datetime.datetime.now())}</small>"""
    
    if view_print == 'full':
        response += f"""
<small>date_utc = {str(datetime.datetime.utcnow())}</small>
<small>mime_type = {str(mime_type)}</small>
<small>ip_address = {str(internal_ip)}</small>
<small>free_mem = {str(free_mem)}</small>dock
"""
    if view_print == 'full':
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
        printing(f'{str_request}: - SLEEPING_FROM_GET({sleep_time})...', print_logs=print_logs)
        sleep(sleep_time)
    except:
        printing(f'{str_request}: - SLEEPING_FROM_ENV({SLEEP_TIME})...', print_logs=print_logs)
        sleep(float(SLEEP_TIME))
        pass
    
    if view_print != 'none':
        message = f'<pre>{response}\n</pre>'
    if view_print == 'full':
        message += f'<pre>env = {ENV}</pre>'
    for line in message.splitlines():
        message_code += f'{str_request}: {line}\n'
    printing(message_code, print_logs=print_logs)
    message_code = f'{platform.node()} \n{message_code} \nhostname:{platform.node()}'
    return message_code, mime_type, status_code, message_code


def ping(host, count='3', wait='5'):
    command = ['ping', '-c', count, '-W', wait, host]
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
            res = requests.get(url, headers=headers_data, timeout=MAX_TIMEOUT).text
        elif method == 'POST':
            res = requests.post(url, data=json_data, headers=headers_data, timeout=MAX_TIMEOUT).text
        elif method == 'DELETE':
            res = requests.delete(url, data=json_data, headers=headers_data, timeout=MAX_TIMEOUT).text
        elif method == 'PUT':
            res = requests.put(url, data=json_data, headers=headers_data, timeout=MAX_TIMEOUT).text
        elif method == 'PATCH':
            res = requests.patch(url, data=json_data, headers=headers_data, timeout=MAX_TIMEOUT).text
        else:
            res = 'not supported method'
    except Exception as e:
        res = f'fail for: method:{method}, url:{url}, headers_data:{headers_data}, body_data:{body_data}, -- {e}'
    
    return str(res)

def set_cookies(response, request):
    global COOKIE_VAL

    cookie_out = list([None] * 9)
    cookie_val = request.args.get('set_cookie')
    cookie_val = cookie_val.split(',') if cookie_val else COOKIE_VAL.split(',')
    
    # save global if key is same as enviroment
    if cookie_val[0] == COOKIE_VAL.split(',')[0]:
        COOKIE_VAL = ','.join(cookie_val)

    for i in range(len(cookie_out)):
        if i < len(cookie_val):
            cookie_val.append('')
        if i in [0]:
            cookie_out[i] = str(cookie_val[i]) if cookie_val[i] else 'key-none'
        elif i in [1]:
            cookie_out[i] = str(cookie_val[i]) if cookie_val[i] else 'val-none'
        elif i in [2]:
            cookie_out[i] = int(cookie_val[i]) if cookie_val[i] and cookie_val[i].isdigit() else 3600
        elif i in [3]:
            cookie_out[i] = int(cookie_val[i]) if cookie_val[i] and cookie_val[i].isdigit() else None
        elif i in [6]:
            cookie_out[i] = True if cookie_val[i] in ['True','true','TRUE'] or cookie_val[i] == '' else False
        elif i in [7]:
            cookie_out[i] = True if cookie_val[i] in ['True','true','TRUE'] else False
        elif i in [8]:
            cookie_out[i] = str(cookie_val[i]) if cookie_val[i] else 'None'
        else:
            cookie_out[i] = str(cookie_val[i]) if cookie_val[i] else None

    response.set_cookie(
        key=cookie_out[0],
        value=cookie_out[1],
        max_age=cookie_out[2],
        expires=cookie_out[3],
        path=cookie_out[4],
        domain=cookie_out[5],
        secure=cookie_out[6],
        httponly=cookie_out[7], 
        samesite=cookie_out[8]
    )
    return response


def config_response(request, title, print_logs='false'):
    printing(title)
    resp, mime_type, status_code, message_code = print_request(request, title=title, print_logs=print_logs)
    response = Response(resp, mimetype=mime_type)
    response = set_cookies(response, request)
    return response, status_code