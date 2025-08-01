import db

def get_pets():
    sql = """SELECT p.id, p.name, p.species, p.breed, u.username, COUNT(m.id) total, MAX(m.sent_at) last
             FROM pets p, messages m, users u
             WHERE p.id = m.pet_id AND
             p.user_id = u.id
             GROUP BY p.id
             ORDER BY p.id DESC"""
    return db.query(sql)

def get_pet(pet_id):
    sql = """SELECT p.id, p.name, p.species, p.breed, u.username 
             FROM pets p, users u 
             WHERE p.id = ? AND
             p.user_id = u.id"""
    return db.query(sql, [pet_id])[0]

def add_pet(name, species, breed, user_id):
    sql = "INSERT INTO pets (name, species, breed, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [name, species, breed, user_id])
    pet_id = db.last_insert_id()
    return pet_id

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
    return db.query(sql, [message_id])[0]

def update_message(message_id, content):
    sql = "UPDATE messages SET content = ? WHERE id = ?"
    db.execute(sql, [content, message_id])

def remove_message(message_id):
    sql = "DELETE FROM messages WHERE id = ?"
    db.execute(sql, [message_id])

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