from app import app
import memes
import users
import re
from flask import (render_template, make_response, request, redirect)
from random import randint
import secrets

@app.route('/')
def index():    
    list = memes.get_list()
    return render_template('index.html', username=users.user_name(), count=len(list), memes=list)

@app.route('/search')
def meme_search():
    query = request.args['query']
    results = memes.meme_get_comments()

@app.route('/submit')
def submit_page():
    return render_template('submit.html')

@app.route('/users')
def users_list():
    userlist = users.get_users()
    username = users.user_name()
    return render_template('users.html', username=username, usercount=len(userlist), users=userlist)

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    userdata = users.get_user_profile(user_id)
    username = users.user_name()
    return render_template('user.html', username=username, userdata=userdata)

@app.route('/comment', methods=['POST'])
def comment():
    if request.form['csrf_token'] != users.csrf_token():
        return render_template('error.html', message='Unauthorized form submission.')
    comment = request.form['comment'].strip()
    meme_id = request.form['meme_id']
    username = users.user_name()
    if len(comment) > 0:
        if memes.meme_add_comment(meme_id, comment):
            return redirect(f"/meme/{meme_id}")
        else:
            return "Failed to add comment to database."
    else:
        error_msg = "Your comment was too short! As in 0 characters. Were you kidding?"
        meme_data = memes.meme_get(meme_id)
        meme_comments = memes.meme_get_comments(meme_id)
        return render_template('meme.html', username=username, meme_data=meme_data, meme_comments=meme_comments, error_msg=error_msg)

@app.route('/send', methods=['POST'])
def send():
    if request.form['csrf_token'] != users.csrf_token():
        return render_template('error.html', message='Unauthorized form submission.')
    content = request.form['content']
    imgupload = request.files["file"]
    img_filename = imgupload.filename.lower()
    img_data = imgupload.read()
    if not img_filename.endswith(('.jpg', '.jpeg', '.png', '.gif')): 
        return "JPG, PNG or GIF files only plz."
    if len(img_data) > 1024 * 1024: return "Your meme is too heavy! Whydontcha downsize it a bit (or two)?"
    meme_id = memes.send(img_data, img_filename, content)
    return redirect(f"/meme/{meme_id}")

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
            return render_template('index.html', msg_loginfailed='Wrong username or password!')

@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        username_ok = len(username) >= 6
        password_ok = len(password) >= 8
        print(username_ok)
        print(password_ok)
        if username_ok and password_ok:
            if users.register(username, password):
                return render_template('welcome.html', message='Hi there! Welcome to Memelation...')
            else:
                return render_template('error.html', message='User already exists. Pick a new one!')
        elif username_ok and not password_ok:
            return render_template('error.html', message='Minimum password length is 8 characters!')
        elif not username_ok and password_ok:
            return render_template('error.html', message='Username length must be at least 6 characters and can contain only letters from a-z, A-Z and numbers from 0-9.!')

@app.route('/meme/random')
def meme_random():
    random_id = randint(1, memes.get_meme_amount())
    return redirect(f"/meme/{random_id}")

@app.route('/meme/img/<int:meme_id>')
def meme_img(meme_id):
    img_data = memes.meme_img(meme_id)
    response = make_response(bytes(img_data))
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.route('/meme/<int:meme_id>')
def meme_show(meme_id):
    username = users.user_name()
    if not memes.meme_get(meme_id):
        return render_template('error.html', message='Meme not found.')
    else:
        meme_data = memes.meme_get(meme_id)
        meme_comments = memes.meme_get_comments(meme_id)
        return render_template('meme.html', username=username, meme_data=meme_data, meme_comments=meme_comments)

