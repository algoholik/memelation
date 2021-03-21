from app import app
from flask import render_template, make_response, request, redirect
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
    imgupload = request.files["file"]
    img_filename = imgupload.filename
    img_data = imgupload.read()
    if not img_filename.endswith(".jpg"): return "Invalid filename"
    if len(img_data) > 1024 * 1024: return "Your meme is too heavy! Whydontcha downsize it a bit (or two)?"
    meme_id = memes.send(img_data, img_filename, content)
    return redirect(f'/meme/{meme_id}')
    # return render_template('error.html', message='Viestin lähetys ei onnistunut')

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

@app.route('/meme/img/<int:meme_id>')
def meme_img(meme_id):
    img_data = memes.meme_img(meme_id)
    response = make_response(bytes(img_data))
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.route('/meme/<int:meme_id>')
def meme_show(meme_id):
    return render_template('meme.html', meme_id=meme_id)
