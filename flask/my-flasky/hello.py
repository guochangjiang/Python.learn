#!/usr/bin/env python3

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name

from flask import request
@app.route('/browser')
def browser():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent

#重定向
from flask import redirect
@app.route('/redirect')
def redir():
    return redirect('http://baidu.com')

#错误响应
from flask import abort
@app.route('/user2/<id>')
def get_user(id):
    user = ''
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user

#使用flask-script
from flask.ext.script import Manager
manager = Manager(app)
# ...
if __name__ == '__main__':
    manager.run()

if __name__ == '__main__':
    manager.run(debug=True)

