
from flask import Flask

app=Flask(__name__)
@app.route('/')
@app.route('/index')
def hello_world():
    return 'Hello World!'

if __name__=='__main__':
    #app.debug = True
    app.run(host='114.212.170.95', port=8080)