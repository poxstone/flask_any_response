import os
import asyncio
import datetime
import random
import websockets

WEBSOCKET_PORT = os.environ.get('WEBSOCKET_PORT', '5678')

async def show_time(websocket):
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(message)
        await asyncio.sleep(random.random() * 2 + 1)

async def main():
    async with websockets.serve(show_time, "0.0.0.0", WEBSOCKET_PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())