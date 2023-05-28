import os
import asyncio
import datetime
import random
import websockets
from sys import argv


WEBSOCKET_IP_ALLOW = argv[1] if len(argv) > 1 else os.getenv('WEBSOCKET_IP_ALLOW', '0.0.0.0')
WEBSOCKET_PORT = argv[2] if len(argv) > 2 else os.getenv('WEBSOCKET_PORT', '5678')

# python3 WEBSOCKET/main_server.py "0.0.0.0" "5678"


async def show_time(websocket):
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(message)
        await asyncio.sleep(random.random() * 2 + 1)


async def main():
    async with websockets.serve(show_time, WEBSOCKET_IP_ALLOW, WEBSOCKET_PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    print(f'WEBSOCKET_RUN: WEBSOCKET_IP_ALLOW={WEBSOCKET_IP_ALLOW} WEBSOCKET_PORT={WEBSOCKET_PORT}')
    asyncio.run(main())
