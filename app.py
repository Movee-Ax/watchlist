from flask import Flask
app = Flask(__name__)

@app.route('/home')
def hello():
    return '<h1>sadasdasdasdasddss 三四三sssAa aa三四三  s112a</h1>'
@app.route('/user/<name>')
def user_page(name):
  return 'User:%s' % name