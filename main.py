import os
from flask import Flask, request

app = Flask(__name__)

FULL_METHODS = ['POST', 'GET', 'HEAD', 'PUT', 'DELETE']


def print_request(request):
    response = ''
    for i in dir(request):
      key = str(i)
      if not (key.startswith('_') or key.startswith('__')):
          response = ('{}\n<b>{}</b> = {}'.format(response, key, getattr(request, key)))
    return '<pre>{}\n env = {}<pre>'.format(response,  os.environ)


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
