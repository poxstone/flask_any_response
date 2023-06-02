import os
import random
import string


ENV = os.environ
FULL_METHODS = ['POST', 'GET', 'HEAD', 'PUT', 'DELETE']
PATH_IGNORE = os.getenv('PATH_IGNORE', "favicon.ico,blank,echo.php,proxy.php")
VERSION_DEP = os.getenv('VERSION_DEP', 'nover')
GOOGLE_CLOUD_PROJECT = os.getenv('GOOGLE_CLOUD_PROJECT', '')
REQUEST_STR_LENGTH = os.getenv('REQUEST_STR_LENGTH', '5')
SLEEP_TIME = os.getenv('SLEEP_TIME', '0')
PORT = os.getenv('PORT', '8080')
LOGS_PRINT = os.getenv('LOGS_PRINT', 'true')
lets_token = os.getenv('LETS_TOKEN', '')
CERTFILE_CRT= os.getenv('CERTFILE_CRT', './.certs/tls.crt')
KEYFILE_TLS = os.getenv('KEYFILE_TLS', './.certs/tls.key')
CHAIN_PEM = os.getenv('CHAIN_PEM', './.certs/chain.pem')
STR_GLOBAL = os.getenv('STR_GLOBAL', ''.join(random.choice(string.ascii_lowercase) for i in range(3)) )
GLOBAL_STATE = os.getenv('GLOBAL_STATE', '200')
GRPC_PORT = os.getenv('GRPC_PORT', '50051')
WORKERS = os.getenv('WORKERS', '1')
GRPC_HOST = os.getenv('GRPC_HOST', '127.0.0.1')
GRPC_PORT = os.getenv('GRPC_PORT', '50051')
WEBSOCKET_IP_ALLOW = os.getenv('WEBSOCKET_IP_ALLOW', '0.0.0.0')
WEBSOCKET_PORT = os.getenv('WEBSOCKET_PORT', '5678')
UDP_IP = os.getenv('UDP_IP', '127.0.0.1')
UDP_IP_ALLOW = os.getenv('UDP_IP_ALLOW', '0.0.0.0')
UDP_PORT = os.getenv('UDP_PORT', '5005')
UDP_MESSAGE = os.getenv('UDP_MESSAGE', 'Hello UDP World')

