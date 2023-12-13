import sqlite3

def create_database():
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score INTEGER)")
        connection.commit()
    except sqlite3.Error as e:
        print("Error creating database:", e)
    finally:
        if connection:
            connection.close()

def insert_player(name, score):
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO players (name, score) VALUES (?, ?)", (name, score))
        connection.commit()
    except sqlite3.Error as e:
        print("Error inserting player data:", e)
    finally:
        if connection:
            connection.close()