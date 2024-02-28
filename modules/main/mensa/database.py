import sqlite3
from datetime import datetime

import table2ascii as t2a

class Manage_database:
    def __init__(self, database_name):
        self.conn = self.connect_to_database(database_name)
        self.create_user_table()
        self.create_time_table()

    def connect_to_database(self, database_name):
        conn = sqlite3.connect(database_name)
        return conn

    def create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE
                        )''')
        self.conn.commit()

    def create_time_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_times (
                            user_id INTEGER,
                            time_recorded TEXT,
                            is_constant INTEGER,
                            FOREIGN KEY (user_id) REFERENCES users(id)
                        )''')
        self.conn.commit()

    def add_or_get_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        user_id = cursor.fetchone()
        if user_id:
            return user_id[0]
        else:
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
            self.conn.commit()
            return cursor.lastrowid

    def save_user_time(self, username, time_recorded):
        if not self.validate_time_format(time_recorded):
            print("Ungültiges Zeitformat oder ungültige Stunden/Minuten. Die Zeit wird nicht eingetragen.")
            return

        user_id = self.add_or_get_user(username)
        cursor = self.conn.cursor()
        cursor.execute("SELECT user_id FROM user_times WHERE user_id=?", (user_id,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.execute("UPDATE user_times SET time_recorded=? WHERE user_id=?", (time_recorded, user_id))
        else:
            cursor.execute("INSERT INTO user_times (user_id, time_recorded) VALUES (?, ?)", (user_id, time_recorded))
        self.conn.commit()

    def set_user_time_constant(self, username):
        user_id = self.add_or_get_user(username)
        cursor = self.conn.cursor()

        cursor.execute("SELECT user_id FROM user_times WHERE user_id=?", (user_id,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.execute("UPDATE user_times SET is_constant=? WHERE user_id=?", (1, user_id))
        else:
            return 0
        self.conn.commit()

    def set_user_time_nconstant(self, username):
        user_id = self.add_or_get_user(username)
        cursor = self.conn.cursor()

        cursor.execute("SELECT user_id FROM user_times WHERE user_id=?", (user_id,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.execute("UPDATE user_times SET is_constant=? WHERE user_id=?", (0, user_id))
        else:
            return 0
        self.conn.commit()

    def get_user_times(self, username):
        user_id = self.add_or_get_user(username)
        cursor = self.conn.cursor()
        cursor.execute("SELECT time_recorded FROM user_times WHERE user_id=?", (user_id,))
        times = cursor.fetchall()
        user_times = [time[0] for time in times if time[0] is not None]
        return user_times

    
    def get_all_users_with_times(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT u.username, t.time_recorded FROM users u LEFT JOIN user_times t ON u.id = t.user_id")
        rows = cursor.fetchall()
        user_times_dict = {}
        for row in rows:
            username, time_recorded = row
            if time_recorded is not None:  # Nur Benutzer mit zugewiesenen Zeiten berücksichtigen
                if username not in user_times_dict:
                    user_times_dict[username] = [time_recorded]
                else:
                    user_times_dict[username].append(time_recorded)

        '''finallist = t2a(
                    header=["User", "Zeit"],
                    body=user_times_dict,
                    style=t2a.PresetStyle.thin_compact)'''

        return user_times_dict


        '''finallist = t2a(
                    header=["User", "Zeit"],
                    body=user_times_dict,
                    style=t2a.PresetStyle.thin_compact)'''
        
        return user_times_dict
    
    def remove_user(self, username):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username=?", (username,))
            user_id = cursor.fetchone()
            if user_id:
                user_id = user_id[0]
                cursor.execute("DELETE FROM user_times WHERE user_id=?", (user_id,))
                cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
                self.conn.commit()
                print("Benutzer erfolgreich gelöscht.")
            else:
                print("Benutzer nicht gefunden.")
        except Exception as e:
            print("Fehler beim Löschen des Benutzers:", e)

    def remove_nconstants(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM users WHERE is_constant=0")
            user_ids = cursor.fetchall()
            for user in user_ids:
                cursor.execute("DELETE FROM user_times WHERE user_id=?", (user,))
                cursor.execute("DELETE FROM users WHERE id=?", (user,))
            
            self.conn.commit()
        except Exception as e:
            print("ERROR {e}")


    def striptime(self, time_recorded):
        if ":" not in time_recorded and "." not in time_recorded:
                time_recorded = f"{int(time_recorded):<04d}"
                time_recorded = time_recorded[:2] + ":" + time_recorded[2:]
        for x in time_recorded:
            if x == ":" or x == ".":
                index = time_recorded.index(x)
                time_recorded0 = f"{int(time_recorded[:index]):02}"
                time_recorded1 = f"{int(time_recorded[index+1:]):02}"
                time_recorded = f"{time_recorded0}:{time_recorded1}"
        
        
        return time_recorded

    def validate_time_format(self, time_recorded):
        try:
            time_obj = datetime.strptime(time_recorded, '%H:%M')
            if 0 <= time_obj.hour < 24 and 0 <= time_obj.minute < 60:
                return True
            else:
                return False
        except ValueError:
            return False

    def close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    # Beispiel: Verwendung der Klasse
    user_time_recorder = Manage_database("users.db")

    # Beispiel: Uhrzeit für einen Benutzer speichern
    username = "Max"
    current_time = "0:99"  # Beispiel für ungültige Zeit
    user_time_recorder.save_user_time(username, current_time)

    # Beispiel: Alle Uhrzeiten für einen Benutzer abrufen und ausgeben
    user_times = user_time_recorder.get_user_times(username)
    print(f"Uhrzeiten für Benutzer {username}: {user_times}")

    # Verbindung zur Datenbank schließen
    user_time_recorder.close_connection()
