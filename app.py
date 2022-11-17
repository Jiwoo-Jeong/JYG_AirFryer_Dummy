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

receipe_example = {
    'p_name' : "삼겹살",
    'guide_tcon' : 3,
    'guide_text_01' : "기름받이에 물 넣어주세요",
    'guide_text_02' : "",
    'cource_n' : 2,
    'cource_name' : ['바싹','촉촉'],
    'cource_value' : [[[180,18,1,3],[180,2,1,2],[200,2,1,3]],[[180,18,1,3],[180,2,1,2]]]
}

# Azure Flask 소스코드 포함부분, 접속확인위해서 남겨놓음
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


@app.route('/view_log', methods=['POST'])
def view_log():
    global log
    rt = ""
    for i in log:
        rt+=i +"\n"
    r = make_response(rt,200)
    r.mimetype = "text/plain"
    return r


# 실제 서버 더미 코드 
# 로그 수신
"""
{
  "Serial": "1280936210",
  "TimeStamp": "1667973287",
  "Pcode": "asd31213wsnw",
}
"""
@app.route('/log', methods=['POST','GET'])
def add_log():
    update_log("/log : "+request.data.decode())
    return {'result':'ok'}


# qr 입력 수신
"""
{
  "Serial": "1280936210",
  "TimeStamp": "1667973287",
  "Pcode": "asd31213wsnw",
}
"""
@app.route('/qr', methods=['POST','GET'])
def qr():
    update_log("/qr : "+request.data.decode())
    return receipe_example



# 계정 연동
"""
{
  "Serial": "1280936210",
  "TimeStamp": "1667973287",
  "action": "login",                    // "action": "logout"
  "user_id": "jwjeong"
}
"""

@app.route('/account', methods=['POST','GET'])
def account():
    update_log("/account : "+request.data.decode())
    return {'result':'ok'}

def update_log(text):
    global log
    log.append(("["+time.asctime()+"]    "+text))
    if len(log) > 40:
        log.pop(0)

if __name__ == '__main__':
    app.run(app = app,ssl_context=ssl_context)
