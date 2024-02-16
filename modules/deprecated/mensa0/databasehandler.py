import sqlite3
from datetime import datetime

# Verbindung zur Datenbank herstellen (falls nicht vorhanden, wird eine neue Datenbank erstellt)
def connect_to_database(database_name):
    conn = sqlite3.connect(database_name)
    return conn

# Benutzertabelle erstellen, falls sie nicht existiert
def create_user_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE
                    )''')
    conn.commit()

# Uhrzeitentabelle erstellen, falls sie nicht existiert
def create_time_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_times (
                        user_id INTEGER,
                        time_recorded TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )''')
    conn.commit()

# Benutzer hinzufügen oder abrufen
def add_or_get_user(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    user_id = cursor.fetchone()
    if user_id:
        return user_id[0]
    else:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        return cursor.lastrowid

# Uhrzeit für einen bestimmten Benutzer speichern
def save_user_time(conn, username, time_recorded):
    user_id = add_or_get_user(conn, username)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_times (user_id, time_recorded) VALUES (?, ?)", (user_id, time_recorded))
    conn.commit()

# Beispiel: Alle Uhrzeiten für einen bestimmten Benutzer abrufen
def get_user_times(conn, username):
    user_id = add_or_get_user(conn, username)
    cursor = conn.cursor()
    cursor.execute("SELECT time_recorded FROM user_times WHERE user_id=?", (user_id,))
    times = cursor.fetchall()
    return [time[0] for time in times]

# Beispiel: Verbindung zur Datenbank herstellen
conn = connect_to_database("example.db")

# Benutzertabelle und Uhrzeitentabelle erstellen
create_user_table(conn)
create_time_table(conn)

# Beispiel: Uhrzeit für einen Benutzer speichern
username = "Max"
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
save_user_time(conn, username, current_time)

# Beispiel: Alle Uhrzeiten für einen Benutzer abrufen und ausgeben
user_times = get_user_times(conn, username)
print(f"Uhrzeiten für Benutzer {username}: {user_times}")

# Verbindung zur Datenbank schließen
conn.close()
