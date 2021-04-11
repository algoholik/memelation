from database import database
import users

def get_list():
    sql = 'SELECT M.content, U.username, M.created, M.id, U.id FROM memes M, users U WHERE M.user_id=U.id ORDER BY M.id'
    result = database.session.execute(sql)
    return result.fetchall()

def get_meme_amount():
    sql = 'SELECT MAX(id) FROM memes'
    result = database.session.execute(sql).fetchone()[0]
    return result

def send(img_data, img_filename, content):
    user_id = users.user_id()
    if user_id == 0: return False
    visible = True
    sql = 'INSERT INTO memes (filename, content, user_id, visible, created, img_data) VALUES (:filename, :content, :user_id, :visible, NOW(), :img_data) RETURNING id'
    result = database.session.execute(sql, {'filename': img_filename, 'content': content, 'user_id': user_id, 'visible': visible, 'img_data': img_data})
    database.session.commit()
    meme_id = result.fetchone()[0]
    return meme_id

def meme_img(meme_id):
    sql = 'SELECT img_data FROM memes WHERE id=:id'
    result = database.session.execute(sql, {'id': meme_id})
    return result.fetchone()[0]

def meme_get(meme_id):
    try:
        sql = 'SELECT M.id, M.filename, M.content, M.user_id, M.created, U.username FROM users U, memes M WHERE M.id=:id AND M.user_id=U.id AND M.visible=True'
        result = database.session.execute(sql, {'id': meme_id})
        return result.fetchone()
    except:
        return False

def meme_get_comments(meme_id):
    try:
        sql = 'SELECT U.username, C.id, C.user_id, C.meme_id, C.content, C.created FROM users U, comments C WHERE U.id=C.user_id AND C.meme_id=:meme_id'
        result = database.session.execute(sql, {'meme_id': meme_id}).fetchall()
        return result
    except:
        return False

def meme_add_comment(meme_id, content):
    user_id = users.user_id()
    visible = True
    try:
        sql = 'INSERT INTO comments (user_id, meme_id, content, visible, created) VALUES (:user_id, :meme_id, :content, :visible, NOW())'
        database.session.execute(sql, {'user_id': user_id, 'meme_id': meme_id, 'content': content, 'visible': visible})
        database.session.commit()
        return True
    except:
        return False