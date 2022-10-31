from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory ,make_response
import ssl
import asyncio
import ssl
import websockets
import time
import asyncio
import threading


async def echo(websocket):
    async for message in websocket:
        global log
        log.append("["+time.asctime()+"] >>> "+message)
        await websocket.send(message)
        log.append("["+time.asctime()+"] <<< "+message)

async def main2():
    async with websockets.serve(echo, "localhost", 8765, ssl=ssl_context):
        await asyncio.Future()  # run forever

def run_ws():
    print("ws server started")
    asyncio.run(main2())

app = Flask(__name__)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

global log
log = ["["+time.asctime()+"] server started"]

thread1 = threading.Thread(target=run_ws)
thread1.daemon = True
thread1.start()

@app.route('/')
def index():
   print('Request for index page rSeceived')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


@app.route('/log', methods=['POST','GET'])
def send_log():
    global log
    rt = ""
    for l in log:
        rt += l +"\n";
    r = make_response(rt,200)
    r.mimetype = "text/plain"
    return r

@app.route('/clear', methods=['POST','GET'])
def clear():
    global log
    log = ["["+time.asctime()+"] log cleared!"]
    rt = ""
    for l in log:
        rt += l +"\n";
    r = make_response(rt,200)
    r.mimetype = "text/plain"
    return r



if __name__ == '__main__':
    app.run(app,ssl_context=ssl_context)