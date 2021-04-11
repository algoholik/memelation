from app import app
from flask import render_template, make_response, request, redirect
import memes, users

@app.route('/')
def index():
    list = memes.get_list()
    username = users.user_name()
    return render_template('index.html', username=username, count=len(list), memes=list)

@app.route('/users')
def users_list():
    userlist = users.get_users()
    username = users.user_name()
    return render_template('users.html', username=username, usercount=len(userlist), users=userlist)

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    userdata = users.get_user_profile(user_id)
    return render_template('user.html', userdata=userdata)

@app.route("/comment", methods=["POST"])
def comment():
    comment = request.form["comment"]
    meme_id = request.form["meme_id"]
    if len(comment) > 0:
        if memes.meme_add_comment(meme_id, comment):
            return redirect(f"/meme/{meme_id}")
        else:
            return "Failed to add comment to database."
    else:
        return render_template('meme.html', msg_commentfailed='Your comment must contain text!')

@app.route("/send", methods=['POST'])
def send():
    content = request.form['content']
    imgupload = request.files["file"]
    img_filename = imgupload.filename
    img_data = imgupload.read()
    if not img_filename.endswith((".jpg", ".jpeg", ".png", ".gif")): 
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
            return render_template('error.html', message='Registration failed.')

@app.route('/meme/img/<int:meme_id>')
def meme_img(meme_id):
    img_data = memes.meme_img(meme_id)
    response = make_response(bytes(img_data))
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.route('/meme/<int:meme_id>')
def meme_show(meme_id):
    if not memes.meme_get(meme_id):
        return render_template('error.html', message='Meme not found.')
    else:
        meme_data = memes.meme_get(meme_id)
        meme_comments = memes.meme_get_comments(meme_id)
        return render_template('meme.html', meme_data=meme_data, meme_comments=meme_comments)

