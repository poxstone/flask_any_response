import os
import random
import string
import json


ENV = os.environ
STR_GLOBAL = os.getenv('STR_GLOBAL', ''.join(random.choice(string.ascii_lowercase) for i in range(3)) )
GLOBAL_STATE = os.getenv('GLOBAL_STATE', '200')
VERSION_DEP = os.getenv('VERSION_DEP', 'nover')
WORKERS = os.getenv('WORKERS', '1')
GOOGLE_CLOUD_PROJECT = os.getenv('GOOGLE_CLOUD_PROJECT', '')
LOCATION = os.getenv('LOCATION', 'us-central1')
SLEEP_TIME = os.getenv('SLEEP_TIME', '0')
MAX_TIMEOUT = int(os.getenv('MAX_TIMEOUT', '30'))
LOGS_PRINT = os.getenv('LOGS_PRINT', 'true')
lets_token = os.getenv('LETS_TOKEN', '')
CERTFILE_CRT= os.getenv('CERTFILE_CRT', './.certs/tls.crt')
KEYFILE_TLS = os.getenv('KEYFILE_TLS', './.certs/tls.key')
CHAIN_PEM = os.getenv('CHAIN_PEM', './.certs/chain.pem')
PORT = os.getenv('PORT', '8080')
GRPC_PORT = os.getenv('GRPC_PORT', '50051')
GRPC_HOST = os.getenv('GRPC_HOST', '127.0.0.1')
GRPC_PORT = os.getenv('GRPC_PORT', '50051')
WEBSOCKET_IP_ALLOW = os.getenv('WEBSOCKET_IP_ALLOW', '0.0.0.0')
WEBSOCKET_PORT = os.getenv('WEBSOCKET_PORT', '5678')
UDP_IP = os.getenv('UDP_IP', '127.0.0.1')
UDP_IP_ALLOW = os.getenv('UDP_IP_ALLOW', '0.0.0.0')
UDP_PORT = os.getenv('UDP_PORT', '5005')
UDP_MESSAGE = os.getenv('UDP_MESSAGE', 'Hello UDP World')
VIEW_PRINT = os.getenv('VIEW_PRINT', 'full')  # full simple none
           # key(llave1),value(valor1),max_age(3600),expires(Date),path(/hola),domain(domain.com),secure(False require Strict),httponly,samesite(None,Lax,Strict)
COOKIE_VAL = os.getenv('COOKIE_VAL', 'fla-key1,fla-value1,3600,,,,True,False,None')

PATH_IGNORE = os.getenv('PATH_IGNORE', "favicon.ico,blank,echo.php,proxy.php")
FULL_METHODS = ['POST', 'GET', 'HEAD', 'PUT', 'DELETE']
REQUEST_STR_LENGTH = os.getenv('REQUEST_STR_LENGTH', '5')  # for randoms strings default (downloads name an requests)

SECRETS_MS_TEAMS = json.loads(os.getenv('SECRETS_MS_TEAMS', '{"vnt-bot-teams-00": { "TEAMS_APP_ID": "84ff6681-3128-4cd9-9039-............", "TEAMS_APP_PASSWORD": "5Jt8Q~yhtDx8hFPXddebKPegw5sV............", "TEAMS_TENANT_ID": "5fcccfc8-ac44-4c9c-8b1e-............", "TEAMS_AUTO_RESPONSE": "Hola respuesta espejo", "GCP_DIALOGF_AGENT_ID":"5765ef52-78f3-47aa-91b8-............" }}'))
