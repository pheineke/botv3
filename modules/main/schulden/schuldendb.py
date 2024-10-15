from datetime import datetime
import shutil
import sqlite3
import time

class Schuldenverwaltung:
    def __init__(self, db_name='./lib/data/db/schulden.db'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_table()

        # self.conn_log = sqlite3.connect("schulden_log.db")
        # self.c_log = self.conn_log.cursor()
        self.create_log()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS Schulden (
                            id INTEGER PRIMARY KEY,
                            schuldner TEXT NOT NULL,
                            glaeubiger TEXT NOT NULL,
                            betrag REAL NOT NULL,
                            comment TEXT
                         )''')
        self.conn.commit()

    def create_log(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS transaction_log (
                            id INTEGER PRIMARY KEY,
                            aktion TEXT NOT NULL,
                            schuldner TEXT NOT NULL,
                            glaeubiger TEXT NOT NULL,
                            betrag REAL NOT NULL,
                            zeit TEXT NOT NULL,
                            comment TEXT NOT NULL
                         )''')
        self.conn.commit()

    def log_transaction(self, aktion, schuldner, glaeubiger, betrag, comment=""):
        zeit = time.strftime('%Y-%m-%d %H:%M:%S')
        self.c.execute("INSERT INTO transaction_log (aktion, schuldner, glaeubiger, betrag, zeit, comment) VALUES (?, ?, ?, ?, ?, ?)",
                            (aktion, schuldner, glaeubiger, betrag, zeit, comment))
        self.conn.commit()

    def backup_database(self, backup_filename=f"backup_{datetime.now()}.db"):
    # Kopiere die aktuelle Datenbankdatei
        backup_path = "./lib/pic/backups/schulden/" + backup_filename
        shutil.copyfile("schulden.db", backup_path)
        return backup_path

    def schulden_hinzufuegen(self, schuldner, glaeubiger, betrag, comment=None):
        self.c.execute("SELECT betrag FROM Schulden WHERE schuldner=? AND glaeubiger=?", (schuldner, glaeubiger))
        result = self.c.fetchone()
        if result and comment:
            vorhandener_betrag = result[0]
            neuer_betrag = vorhandener_betrag + betrag
            self.c.execute("UPDATE Schulden SET betrag=? WHERE schuldner=? AND glaeubiger=? AND comment=?", (neuer_betrag, schuldner, glaeubiger, comment))
            self.conn.commit()
            self.log_transaction("Schulden hinzugefügt", schuldner, glaeubiger, betrag, comment)
            return f"Schulden von {schuldner} zu {glaeubiger} um {betrag} erhöht. Neue Gesamtschulden: {neuer_betrag}."
        elif result:
            vorhandener_betrag = result[0]
            neuer_betrag = vorhandener_betrag + betrag
            self.c.execute("UPDATE Schulden SET betrag=? WHERE schuldner=? AND glaeubiger=?", (neuer_betrag, schuldner, glaeubiger))
            self.conn.commit()
            self.log_transaction("Schulden hinzugefügt", schuldner, glaeubiger, betrag, comment)
            return f"Schulden von {schuldner} zu {glaeubiger} um {betrag} erhöht. Neue Gesamtschulden: {neuer_betrag}."
        else:
            self.c.execute("INSERT INTO Schulden (schuldner, glaeubiger, betrag) VALUES (?, ?, ?)", (schuldner, glaeubiger, betrag))
            self.conn.commit()
            self.log_transaction("Schulden hinzugefügt", schuldner, glaeubiger, betrag, comment)
            return f"Schulden von {schuldner} zu {glaeubiger} in Höhe von {betrag} hinzugefügt."

    def schulden_tilgen(self, schuldner, glaeubiger, betrag, comment=None):
        if comment:
            self.c.execute("SELECT betrag FROM Schulden WHERE schuldner=? AND glaeubiger=? AND comment=?", (schuldner, glaeubiger, comment))
            result = self.c.fetchone()
            if result:
                vorhandener_betrag = result[0]
                if vorhandener_betrag >= betrag:
                    neuer_betrag = vorhandener_betrag - betrag
                    self.c.execute("UPDATE Schulden SET betrag=? WHERE schuldner=? AND glaeubiger=?", (neuer_betrag, schuldner, glaeubiger))
                    self.conn.commit()
                    self.log_transaction("Schulden getilgt", schuldner, glaeubiger, betrag)
                    return f"Schulden von {schuldner} zu {glaeubiger} um {betrag} verringert."
                else:
                    return "Der angegebene Betrag ist größer als die vorhandenen Schulden."
            else:
                return "Keine Schulden gefunden."
        else:
            self.c.execute("SELECT betrag FROM Schulden WHERE schuldner=? AND glaeubiger=?", (schuldner, glaeubiger))
            result = self.c.fetchone()
            if result:
                vorhandener_betrag = result[0]
                if vorhandener_betrag >= betrag:
                    neuer_betrag = vorhandener_betrag - betrag
                    self.c.execute("UPDATE Schulden SET betrag=? WHERE schuldner=? AND glaeubiger=?", (neuer_betrag, schuldner, glaeubiger))
                    self.conn.commit()
                    self.log_transaction("Schulden getilgt", schuldner, glaeubiger, betrag)
                    return f"Schulden von {schuldner} zu {glaeubiger} um {betrag} verringert."
                else:
                    return "Der angegebene Betrag ist größer als die vorhandenen Schulden."
            else:
                return "Keine Schulden gefunden."

    def schulden_anzeigen(self, schuldner=None, glaeubiger=None):
        if schuldner and glaeubiger:
            self.c.execute("SELECT betrag FROM Schulden WHERE schuldner=? AND glaeubiger=? AND comment", (schuldner, glaeubiger))
            result = self.c.fetchone()
            if result:
                return f"Schulden von {schuldner} zu {glaeubiger}: {result[0]}"
            else:
                return "Keine Schulden gefunden."
        elif schuldner:
            self.c.execute("SELECT glaeubiger, betrag FROM Schulden WHERE schuldner=?", (schuldner,))
            results = self.c.fetchall()
            if results:
                returnstring = "" #f"Schulden von {schuldner}:\n"
                for row in results:
                    returnstring += f"{row[0]}: {row[1]}\n"
                return returnstring
            else:
                print("Keine Schulden gefunden.")
        elif glaeubiger:
            self.c.execute("SELECT schuldner, betrag FROM Schulden WHERE glaeubiger=?", (glaeubiger,))
            results = self.c.fetchall()
            if results:
                returnstring = "" #f"Schulden bei {glaeubiger}:\n"
                for row in results:
                    returnstring += f"{row[0]}: {row[1]}\n"
                return returnstring
            else:
                return "Keine Schulden gefunden."
        else:
            return "Ungültige Anfrage."

    def alle_schulden_anzeigen(self):
        self.c.execute("SELECT schuldner, glaeubiger, betrag FROM Schulden")
        results = self.c.fetchall()
        if results:
            return results
        else:
            return "Keine Schulden gefunden."

    def aktualisieren(self):
        liste = self.alle_schulden_anzeigen()
        if type(liste) is not list:
            return
        else:
            usera = None
            userb = None
            betragab = None
            for userx, usery, betragxy in liste:
                if userx == userb and usery == usera:
                    if betragxy > betragab:
                        betrag0 = betragxy - betragab
                        betrag1 = betragxy - betrag0
                        self.schulden_tilgen(userx, usery, round(betrag1, 2))
                        self.schulden_tilgen(usera, userb, round(betrag1, 2))
                    elif betragxy < betragab:
                        betrag0 = betragab - betragxy
                        betrag1 = betragab - betrag0
                        self.schulden_tilgen(userx, usery, round(betragxy, 2))
                        self.schulden_tilgen(usera, userb, round(betrag1, 2))
                    else:  # ==
                        self.schulden_tilgen(userx, usery, betragab)
                        self.schulden_tilgen(usery, userx, betragab)
                        #print(f"c {userx} {usery} {usera} {userb} {betragxy} {betragab}")

                else:
                    usera = userx
                    userb = usery
                    betragab = betragxy

            liste = self.alle_schulden_anzeigen()
            for userx, usery, betragxy in liste:
                self.c.execute("DELETE FROM Schulden WHERE betrag=0.0")
                self.conn.commit()

    def __del__(self):
        self.conn.close()