from database import database
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = 'SELECT password, id, username FROM users WHERE username=:username'
    result = database.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user == None: return False
    else:
        if check_password_hash(user[0], password):
            session['user_id'] = user[1]
            session['username'] = user[2]
            return True
        else: return False

def logout():
    del session['user_id']

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = 'INSERT INTO users (username, password, created) VALUES (:username, :password, NOW())'
        database.session.execute(sql, {'username': username, 'password': hash_value})
        database.session.commit()
    except: 
        return False
    finally: 
        return login(username, password)

def user_id():
    return session.get('user_id', 0)

def user_name():
    return session.get('username', 0)

def get_users():
    sql = 'SELECT U.username, U.created FROM users U'
    result = database.session.execute(sql)
    return result.fetchall()
