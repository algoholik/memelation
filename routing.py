from app import app
from flask import render_template, request, redirect
import memes, users

@app.route('/')
def index():
    list = memes.get_list()
    username = users.user_name()
    return render_template('index.html', username=username, count=len(list), memes=list)

@app.route('/users')
def userlist():
    userlist = users.get_users()
    return render_template('users.html', usercount=len(userlist), users=userlist)

@app.route("/send", methods=['POST'])
def send():
    content = request.form['content']
    if memes.send(content):
        return redirect('/')
    else:
        return render_template('error.html', message='Viestin lähetys ei onnistunut')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if users.login(username, password):
            return redirect('/')
        else:
            return render_template('index.html', msg_loginfailed='Väärä tunnus tai salasana')

@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if users.register(username, password):
            return redirect('/')
        else:
            return render_template('error.html', message='Rekisteröinti ei onnistunut')