import sqlite3

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
            print(f"Schulden von {schuldner} zu {glaeubiger} um {betrag} erhöht. Neue Gesamtschulden: {neuer_betrag}.")
        else:
            self.c.execute("INSERT INTO Schulden (schuldner, glaeubiger, betrag) VALUES (?, ?, ?)", (schuldner, glaeubiger, betrag))
            self.conn.commit()
            print(f"Schulden von {schuldner} zu {glaeubiger} in Höhe von {betrag} hinzugefügt.")

    def schulden_tilgen(self, schuldner, glaeubiger, betrag):
        self.c.execute("SELECT betrag FROM Schulden WHERE schuldner=? AND glaeubiger=?", (schuldner, glaeubiger))
        result = self.c.fetchone()
        if result:
            vorhandener_betrag = result[0]
            if vorhandener_betrag >= betrag:
                neuer_betrag = vorhandener_betrag - betrag
                self.c.execute("UPDATE Schulden SET betrag=? WHERE schuldner=? AND glaeubiger=?", (neuer_betrag, schuldner, glaeubiger))
                self.conn.commit()
                print(f"Schulden von {schuldner} zu {glaeubiger} um {betrag} verringert.")
            else:
                print("Der angegebene Betrag ist größer als die vorhandenen Schulden.")
        else:
            print("Keine Schulden gefunden.")

    def schulden_anzeigen(self, schuldner=None, glaeubiger=None):
        if schuldner and glaeubiger:
            self.c.execute("SELECT betrag FROM Schulden WHERE schuldner=? AND glaeubiger=?", (schuldner, glaeubiger))
            result = self.c.fetchone()
            if result:
                print(f"Schulden von {schuldner} zu {glaeubiger}: {result[0]}")
            else:
                print("Keine Schulden gefunden.")
        elif schuldner:
            self.c.execute("SELECT glaeubiger, betrag FROM Schulden WHERE schuldner=?", (schuldner,))
            results = self.c.fetchall()
            if results:
                print(f"Schulden von {schuldner}:")
                for row in results:
                    print(f"{row[0]}: {row[1]}")
            else:
                print("Keine Schulden gefunden.")
        elif glaeubiger:
            self.c.execute("SELECT schuldner, betrag FROM Schulden WHERE glaeubiger=?", (glaeubiger,))
            results = self.c.fetchall()
            if results:
                print(f"Schulden bei {glaeubiger}:")
                for row in results:
                    print(f"{row[0]}: {row[1]}")
            else:
                print("Keine Schulden gefunden.")
        else:
            print("Ungültige Anfrage.")

    def alle_schulden_anzeigen(self):
        self.c.execute("SELECT schuldner, glaeubiger, betrag FROM Schulden")
        results = self.c.fetchall()
        if results:
            return results
        else:
            print("Keine Schulden gefunden.")

    def aktualisieren(self):
        liste = self.alle_schulden_anzeigen()
        for userx, usery, betragxy in liste:
            for usera, userb, betragab in liste:
                if userx == userb and usery == usera:
                    try:
                        betrag0 = betragxy-betragab
                        print(f"{betragxy}-{betragab}-{betrag0}")
                        
                        if betrag0 > 0:
                            self.schulden_tilgen(userx, usery, betrag0)
                            self.schulden_tilgen(usera, userb, betrag0)
                        if betrag0 < 0:
                            self.schulden_tilgen(userx, usery, betrag0)
                            self.schulden_tilgen(usera, userb, betrag0)
                        else:
                            self.schulden_tilgen(userx, usery, betrag0)
                            self.schulden_tilgen(usera, userb, betrag0)
                    except:
                        pass

    def __del__(self):
        self.conn.close()

# Beispielanwendung
schulden_manager = Schuldenverwaltung()
schulden_manager.alle_schulden_anzeigen()
schulden_manager.schulden_hinzufuegen("user0","user1", 50)
schulden_manager.schulden_hinzufuegen("user1","user0", 50)
schulden_manager.aktualisieren()