from database import database
import users

def get_list():
    sql = 'SELECT M.content, U.username, M.created FROM memes M, users U WHERE M.user_id=U.id ORDER BY M.id'
    result = database.session.execute(sql)
    return result.fetchall()

def send(content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = 'INSERT INTO memes (content, user_id, created) VALUES (:content, :user_id, NOW())'
    database.session.execute(sql, {'content': content, 'user_id': user_id})
    database.session.commit()
    return True
