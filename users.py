from werkzeug.security import check_password_hash, generate_password_hash
import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if len(result) == 1:
        user_id, password_hash = result[0]
        if check_password_hash(password_hash, password):
            return user_id

    return None

def get_user(user_id):
    sql = """SELECT id, username, image IS NOT NULL has_image
             FROM users
             WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_messages(user_id):
    sql = """SELECT m.id,
                    m.pet_id,
                    p.name pet_name,
                    m.sent_at
             FROM pets p, messages m
             WHERE p.id = m.pet_id AND
                   m.user_id = ?
             ORDER BY m.sent_at DESC"""
    return db.query(sql, [user_id])

def get_pets(user_id):
    sql = """SELECT id,
                    name,
                    species,
                    breed
             FROM pets
             WHERE user_id = ?
             ORDER BY name"""
    return db.query(sql, [user_id])

def update_image(user_id, image):
    sql = "UPDATE users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])

def get_image(user_id):
    sql = "SELECT image FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None

def remove_image(user_id):
    sql = "UPDATE users SET image = null WHERE id = ?"
    db.execute(sql, [user_id])