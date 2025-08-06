import db

def get_pets():
    sql = """SELECT p.id, p.name, p.species, p.breed, u.username, p.user_id,
             COUNT(m.id) total, MAX(m.sent_at) last
             FROM pets p
             LEFT JOIN messages m ON p.id = m.pet_id
             JOIN users u ON p.user_id = u.id
             GROUP BY p.id, p.name, p.species, p.breed, u.username
             ORDER BY p.id DESC"""
    return db.query(sql)

def get_pet(pet_id):
    sql = """SELECT p.id, p.name, p.species, p.breed, u.username, p.user_id 
             FROM pets p, users u 
             WHERE p.id = ? AND
             p.user_id = u.id"""
    result = db.query(sql, [pet_id])
    return result[0] if result else None

def add_pet(name, species, breed, user_id):
    sql = "INSERT INTO pets (name, species, breed, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [name, species, breed, user_id])
    pet_id = db.last_insert_id()
    return pet_id

def update_pet(pet_id, name, species, breed):
    sql = """UPDATE pets 
             SET name = ?, 
                 species = ?,
                 breed = ?
             WHERE id = ?"""
    db.execute(sql, [name, species, breed, pet_id])

def remove_pet(pet_id):
    sql = "DELETE FROM pets WHERE id = ?"
    db.execute(sql, [pet_id])

def update_image(pet_id, image):
    sql = "UPDATE pets SET image = ? WHERE id = ?"
    db.execute(sql, [image, pet_id])

def get_image(pet_id):
    sql = "SELECT image FROM pets WHERE id = ?"
    result = db.query(sql, [pet_id])
    return result[0][0] if result else None

def add_message(content, user_id, pet_id):
    sql = """INSERT INTO messages (content, sent_at, user_id, pet_id)
             VALUES (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, pet_id])

def get_messages(pet_id):
    sql = """SELECT m.id, m.content, m.sent_at, m.user_id, u.username
             FROM messages m, users u
             WHERE m.user_id = u.id AND m.pet_id = ?
             ORDER BY m.id"""
    return db.query(sql, [pet_id])

def get_message(message_id):
    sql = "SELECT id, content, user_id, pet_id FROM messages WHERE id = ?"
    result = db.query(sql, [message_id])
    return result[0] if result else None

def update_message(message_id, content):
    sql = "UPDATE messages SET content = ? WHERE id = ?"
    db.execute(sql, [content, message_id])

def remove_message(message_id):
    sql = "DELETE FROM messages WHERE id = ?"
    db.execute(sql, [message_id])

def remove_all_messages(pet_id):
    sql = "DELETE FROM messages WHERE pet_id = ?"
    db.execute(sql, [pet_id])

def search(query): #hakee viestin sisällöstä
    sql = """SELECT m.id message_id,
                    m.pet_id,
                    p.name pet_name,
                    p.breed,
                    p.species,
                    m.sent_at,
                    u.username
             FROM pets p, messages m, users u
             WHERE p.id = m.pet_id AND
                   u.id = m.user_id AND
                   m.content LIKE ? 
             ORDER BY m.sent_at DESC"""
    return db.query(sql, ["%" + query + "%"])