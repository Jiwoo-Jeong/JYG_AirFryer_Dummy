import asyncio
import ssl
import websockets
import time
import asyncio
from aiohttp import web
from typing import List
import threading , sys


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

global log
log = ["["+time.asctime()+"] server started"]

async def echo(websocket):
    async for message in websocket:
        global log
        log.append("["+time.asctime()+"] >>> "+message)
        await websocket.send(message)
        log.append("["+time.asctime()+"] <<< "+message)

async def main2():
    async with websockets.serve(echo, "localhost", 8765, ssl=ssl_context):
        await asyncio.Future()  # run forever

async def hello(request):
    global log
    rt = ""
    for l in log:
        rt += l +"\n";
    return web.Response(text=rt)

async def clear(request):
    global log
    log = ["["+time.asctime()+"] log cleared!"]
    rt = ""
    for l in log:
        rt += l +"\n";
    return web.Response(text=rt)

def run_ws():
    asyncio.run(main2())

if __name__ == "__main__":
    try:
        app = web.Application()
        app.router.add_get('/', hello)
        app.router.add_get('/clear', clear)

        thread1 = threading.Thread(target=run_ws)
        thread1.start()

        web.run_app(app)
    except KeyboardInterrupt:
        sys.exit()

"""


import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with websockets.serve(hello, "localhost", 8765, ssl=ssl_context):
        await asyncio.Future()  # run forever

async def hello(request):
    return web.Response(text="Hello, world")

if __name__ == "__main__":
    asyncio.run(main())

    app = web.Application()
    #l: List[web.WebSocketResponse] = []
    #app[websockets] = l
    app.router.add_get('/', hello)
    
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    web.run_app(app,loop=loop)
    """