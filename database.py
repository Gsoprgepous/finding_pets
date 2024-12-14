import sqlite3

def create_connection():
    conn = sqlite3.connect('pets.db')
    return conn

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, photo_path TEXT, breed TEXT)''')
    conn.commit()
    conn.close()

def add_pet_to_db(user_id, photo_path, breed):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO pets (user_id, photo_path, breed) VALUES (?, ?, ?)", (user_id, photo_path, breed))
    conn.commit()
    conn.close()

def get_found_pets():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM pets WHERE breed IS NOT NULL AND breed != ''")
    rows = c.fetchall()
    conn.close()
    return rows
