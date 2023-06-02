# allow import from previous path
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import asyncio
import datetime
import random
import websockets
from sys import argv

from application.utils import printing
from application.config import WEBSOCKET_IP_ALLOW, WEBSOCKET_PORT, ENV, STR_GLOBAL

WEBSOCKET_IP_ALLOW = argv[1] if len(argv) > 1 else WEBSOCKET_IP_ALLOW
WEBSOCKET_PORT = argv[2] if len(argv) > 2 else WEBSOCKET_PORT
# python3 WEBSOCKET/main_server.py "0.0.0.0" "5678"

printing(f'INSTANCEID_UDP={STR_GLOBAL}')


async def show_time(websocket):
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        random_num = random.random() * 2 + 1
        message_response = f'''{STR_GLOBAL} - {message} - PATH {websocket.path} - UUID:{websocket.id}
- websocket.request_headers: {websocket.request_headers}
- websocket.response_headers: {websocket.response_headers}
- ENV: {ENV}
_ _ _ _ _ _ _ _ _\n
'''
        printing(message_response)
        await websocket.send(f'{message_response}')
        await asyncio.sleep(random_num)


async def main():
    async with websockets.serve(show_time, WEBSOCKET_IP_ALLOW, WEBSOCKET_PORT):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    printing(f'WEBSOCKET_RUN: WEBSOCKET_IP_ALLOW={WEBSOCKET_IP_ALLOW} WEBSOCKET_PORT={WEBSOCKET_PORT}')
    asyncio.run(main())
