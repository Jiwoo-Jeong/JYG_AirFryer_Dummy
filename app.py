from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory ,make_response
import ssl
import time , os 
from flask import request

app = Flask(__name__)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

global log
log = []

global receipe_request
receipe_request = []

receipe_example = { 'PDN':'초신선 무항생제 삼겹살 A','CG1':'기름받이에 물','CG2':'','NUC':'3',
                    'C01':'180_18_1_3',
                    'C02':'180_2_1_2',
                    'C03':'200_2_1_3'}


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


@app.route('/ping', methods=['POST','GET'])
def pong():
    r = make_response("alive",200)
    r.mimetype = "text/plain"
    return r

@app.route('/clear_log', methods=['POST','GET'])
def clear_log():
    global log
    log = ["["+time.asctime()+"] log cleared!"]
    rt = ""
    for l in log:
        rt += l +"\n"
    r = make_response(rt,200)
    r.mimetype = "text/plain"
    return r

@app.route('/log', methods=['POST','GET'])
def get_log():
    global log
    log.append((time.asctime()+request.data.decode()))
    if len(log) > 20:
        log.pop()
    r = make_response("ok",200)
    r.mimetype = "text/plain"
    return r

@app.route('/view_log', methods=['POST','GET'])
def view_log():
    global log
    rt = ""
    for i in log:
        rt+=i +"\n"
    r = make_response(rt,200)
    r.mimetype = "text/plain"
    return r

@app.route('/qr', methods=['POST','GET'])
def qr():
    global receipe_request
    receipe_request.append(request.data)
    if len(receipe_request) > 20:
        receipe_request.pop()
    return receipe_example

if __name__ == '__main__':
    app.run(app = app,ssl_context=ssl_context)
