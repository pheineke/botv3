import sqlite3
import time

class Schuldenverwaltung:
    def __init__(self, db_name='schulden.db'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS Schulden (
                            id INTEGER PRIMARY KEY,
                            schuldner TEXT NOT NULL,
                            glaeubiger TEXT NOT NULL,
                            betrag REAL NOT NULL
                         )''')
        self.conn.commit()

    def schulden_hinzufuegen(self, schuldner, glaeubiger, betrag):
        # Überprüfen, ob bereits Schulden existieren
        self.c.execute("SELECT betrag FROM Schulden WHERE schuldner=? AND glaeubiger=?", (schuldner, glaeubiger))
        result = self.c.fetchone()
        if result:
            vorhandener_betrag = result[0]
            neuer_betrag = vorhandener_betrag + betrag
            self.c.execute("UPDATE Schulden SET betrag=? WHERE schuldner=? AND glaeubiger=?", (neuer_betrag, schuldner, glaeubiger))
            self.conn.commit()
            return f"Schulden von {schuldner} zu {glaeubiger} um {betrag} erhöht. Neue Gesamtschulden: {neuer_betrag}."
        else:
            self.c.execute("INSERT INTO Schulden (schuldner, glaeubiger, betrag) VALUES (?, ?, ?)", (schuldner, glaeubiger, betrag))
            self.conn.commit()
            return f"Schulden von {schuldner} zu {glaeubiger} in Höhe von {betrag} hinzugefügt."

    def schulden_tilgen(self, schuldner, glaeubiger, betrag):
        self.c.execute("SELECT betrag FROM Schulden WHERE schuldner=? AND glaeubiger=?", (schuldner, glaeubiger))
        result = self.c.fetchone()
        if result:
            vorhandener_betrag = result[0]
            if vorhandener_betrag >= betrag:
                neuer_betrag = vorhandener_betrag - betrag
                self.c.execute("UPDATE Schulden SET betrag=? WHERE schuldner=? AND glaeubiger=?", (neuer_betrag, schuldner, glaeubiger))
                self.conn.commit()
                return f"Schulden von {schuldner} zu {glaeubiger} um {betrag} verringert."
            else:
                return "Der angegebene Betrag ist größer als die vorhandenen Schulden."
        else:
            return "Keine Schulden gefunden."

    def schulden_anzeigen(self, schuldner=None, glaeubiger=None):
        if schuldner and glaeubiger:
            self.c.execute("SELECT betrag FROM Schulden WHERE schuldner=? AND glaeubiger=?", (schuldner, glaeubiger))
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
                #print(f"{userx} {usery} {usera} {userb}")
                #print(f"{userx == userb} {usery == usera}")
                if userx == userb and usery == usera:
                        
                    if betragxy > betragab:
                    #   350         200
                        betrag0 = betragxy-betragab # 350 - 200 = 150
                        betrag1 = betragxy - betrag0 # 350 - 150 = 200
                        #print(f"a {userx} {usery} {usera} {userb} {betragxy} {betragab}")
                        self.schulden_tilgen(userx, usery, betrag1)
                        self.schulden_tilgen(usera, userb, betrag1)
                    elif betragxy < betragab:
                    #   150         200:
                        betrag0 = betragab-betragxy
                        betrag1 = betragab - betrag0
                        #print(f"b {userx} {usery} {usera} {userb} {betragxy} {betragab} {betrag0}")
                        self.schulden_tilgen(userx, usery, betragxy)
                        self.schulden_tilgen(usera, userb, betrag1)
                    else: # ==
                        self.schulden_tilgen(userx, usery, betragab)
                        self.schulden_tilgen(usery, userx, betragab)
                        #print(f"c {userx} {usery} {usera} {userb} {betragxy} {betragab}")

                else:
                    usera = userx
                    userb = usery
                    betragab = betragxy

    def __del__(self):
        self.conn.close()
