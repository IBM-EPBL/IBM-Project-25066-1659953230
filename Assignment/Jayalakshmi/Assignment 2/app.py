from flask import Flask, request, json
from flask import render_template

app = Flask(__name__)
app.debug = True



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/signin", methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username and password:
        return json.dumps({'validation' : validateUser(username, password)})
    return json.dumps({'validation' : False})

def validateUser(username, password):
    return True
    

