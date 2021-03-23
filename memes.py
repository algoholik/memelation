from database import database
import users

def get_list():
    sql = 'SELECT M.content, U.username, M.created, M.id FROM memes M, users U WHERE M.user_id=U.id ORDER BY M.id'
    result = database.session.execute(sql)
    return result.fetchall()

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
        print("ei löydy")
        return False