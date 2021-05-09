from database import database
import users



def get_list():
    sql = '''
        SELECT M.content, U.username, M.created, M.id, U.id 
        FROM memes M, users U 
        WHERE M.user_id=U.id 
        AND M.visible=True
        ORDER BY M.id
    '''
    result = database.session.execute(sql)
    return result.fetchall()



def get_tags(tagword):
    tag_word = tagword.replace("#","").replace(".", "").replace(",", "").strip()
    sql = '''
        SELECT M.content, U.username, M.created, M.id, U.id 
        FROM memes M, users U, tags T, tagging G 
        WHERE M.user_id=U.id 
        AND G.meme_id=M.id 
        AND G.tag_id=T.id 
        AND T.tagword=:tagword
        AND M.visible=True 
        ORDER BY G.id
    '''
    result = database.session.execute(sql, {'tagword': tag_word})
    return result.fetchall()



def get_active_meme_ids():
    sql = '''SELECT id FROM memes WHERE visible=True'''
    result = database.session.execute(sql).fetchall()
    return [just_id[0] for just_id in result]



def send(img_data, img_filename, content, tagwords):
    user_id = users.user_id()
    if user_id == 0: return False
    visible = True
    tags = [tag.replace("#", "").replace(".", "").replace(",", "").strip() for tag in tagwords.split(" ") if tag.startswith("#")]
    sql1 = '''
        INSERT INTO memes (filename, content, user_id, visible, created, img_data) 
        VALUES (:filename, :content, :user_id, :visible, NOW(), :img_data) 
        RETURNING id
    '''
    result1 = database.session.execute(
        sql1, {
            'filename': img_filename, 
            'content': content, 
            'user_id': user_id, 
            'visible': visible, 
            'img_data': img_data
        }
    )
    meme_id = result1.fetchone()[0]
    for word in tags:
        sql2 = '''INSERT INTO tags (tagword) SELECT :tagword WHERE NOT EXISTS (SELECT 1 FROM tags WHERE tagword=:tagword)'''
        database.session.execute(sql2, {'tagword': word})
        sql3 = '''SELECT id FROM tags WHERE tagword=:tagword'''
        result2 = database.session.execute(sql3, {'tagword': word})
        tag_id = result2.fetchone()[0]
        sql4 = '''INSERT INTO tagging (meme_id, tag_id) VALUES (:meme_id, :tag_id)'''
        database.session.execute(sql4, {'meme_id': meme_id, 'tag_id': tag_id})
    database.session.commit()
    return meme_id



def meme_img(meme_id):
    sql = '''
        SELECT img_data FROM memes WHERE id=:id
    '''
    result = database.session.execute(
        sql, {
            'id': meme_id
        }
    )
    return result.fetchone()[0]



def meme_get(meme_id):
    try:
        sql = '''
            SELECT M.id, M.filename, M.content, M.user_id, M.created, U.username 
            FROM users U, memes M 
            WHERE M.id=:id 
            AND M.user_id=U.id 
            AND M.visible=True
        '''
        result = database.session.execute(
            sql, {
                'id': meme_id
            }
        )
        return result.fetchone()
    except:
        return False



def meme_get_comments(meme_id):
    try:
        sql = '''
            SELECT U.username, C.id, C.user_id, C.meme_id, C.content, C.created 
            FROM users U, comments C 
            WHERE U.id=C.user_id 
            AND C.meme_id=:meme_id
            AND C.visible=True
        '''
        result = database.session.execute(
            sql, {
                'meme_id': meme_id
            }
        ).fetchall()
        return result
    except:
        return False


def meme_get_tags(meme_id):
    try:
        sql = '''
            SELECT T.tagword 
            FROM tags T, tagging G 
            WHERE T.id=G.tag_id
            AND G.meme_id=:meme_id
        '''
        result = database.session.execute(
            sql, {
                'meme_id': meme_id
            }
        ).fetchall()
        return [tagword[0] for tagword in result]
    except:
        return False



def meme_add_comment(meme_id, content):
    user_id = users.user_id()
    visible = True
    try:
        sql = '''
            INSERT INTO comments (user_id, meme_id, content, visible, created) 
            VALUES (:user_id, :meme_id, :content, :visible, NOW())
        '''
        database.session.execute(
            sql, {
                'user_id': user_id, 
                'meme_id': meme_id, 
                'content': content, 
                'visible': visible
            }
        )
        database.session.commit()
        return True
    except:
        return False
