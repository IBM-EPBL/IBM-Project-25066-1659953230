from flask import Flask, render_template, request, redirect, url_for, session
import re
import ibm_db
import os
import json
global j
app = Flask(__name__)
job=""
app.secret_key='a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=nmc63120;PWD=BC9ub7wWLk2Yb8fM;",'','')

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
            return render_template('register.html', msg = msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO  users VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg = msg)
        else:
            msg = 'Incorrect Username / Password!'
    return render_template('login.html', msg = msg)

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

@app.route('/display')
def display():
    try:
        username = session['username']
    except:
        return render_template('home.html',msg='Please login first')
    print(username)
    sql = "SELECT * FROM jobs WHERE username =?"
    stmt = ibm_db.prepare(conn, sql)
    print(stmt) 
    ibm_db.bind_param(stmt,1,username)
    ibm_db.execute(stmt)
    print(stmt) 
    account = ibm_db.fetch_assoc(stmt)
    print ("display",account)
    

    # print(session["username"],session['id'])
    # sql = "SELECT username FROM jobs WHERE username =?"
    # stmt=ibm_db.prepare(conn,sql)
    # ibm_db.bind_param(stmt,1,session['username'])
    # ibm_db.execute(stmt)
    # account = ibm_db.fetch_assoc(stmt)
    # print("accountdislay",account)
    return render_template('display.html',account = account)

@app.route('/logout')
def logout():
   session['loggedin'] = False
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('reg', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat('./static/css/reg.css').st_mtime)
    return url_for(endpoint, **values)

@app.route('/home')
def home():
    msg=session['loggedin']
    return render_template('home.html',msg=msg)

@app.route('/apply/<job>')
def getJob(job):
    print(job)
    insert_sql = "INSERT INTO jobs (username, job) VALUES (?, ?)"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, session['username'])
    ibm_db.bind_param(prep_stmt, 2, job)
    ibm_db.execute(prep_stmt)
    session['loggedin'] = True
    return redirect(url_for('apply'))

@app.route('/apply',methods =['GET', 'POST'])
def apply():
    msg=''
    try:
        print(session['id'])
    except:
        return render_template('apply.html',msg='Something went wrong')
    if request.method == 'POST' :
        print(job)
        username = session['username']
        qualification= request.form['qualification']
        skills = request.form['skills']
        categ = request.form['s']
        insert_sql = "UPDATE jobs SET QUALIFICATION = ?, SKILLS = ?, CATEGORY = ? WHERE USERNAME = ?"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, qualification)
        ibm_db.bind_param(prep_stmt, 2, skills)
        ibm_db.bind_param(prep_stmt, 3, categ)
        ibm_db.bind_param(prep_stmt, 4, username)
        ibm_db.execute(prep_stmt)
        msg = 'You have successfully applied for '+job+' !'
        session['loggedin'] = True
        return render_template('dashboard.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('apply.html', msg = msg)

if __name__ == '__main__':
    job=""
    app.run(debug=True)
