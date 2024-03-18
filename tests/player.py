import subprocess
import vlc

# YouTube-URL des Videos
url = "https://www.youtube.com/watch?v=bMt47wvK6u0"

# Verwende youtube-dl, um den direkten Videolink zu erhalten
process = subprocess.Popen(['youtube-dl', '-g', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()

if process.returncode == 0:
    # Extrahiere den Videolink aus der Ausgabe
    playurl = output.decode('utf-8').strip()

    # Erzeuge eine Instanz von VLC
    Instance = vlc.Instance()
    player = Instance.media_player_new()

    # Erzeuge ein Media-Objekt mit dem Videolink
    Media = Instance.media_new(playurl)

    # Setze das Media-Objekt für den Player
    player.set_media(Media)

    # Spiele das Video ab
    player.play()
else:
    print("Fehler beim Abrufen des Videolinks:", error.decode('utf-8'))
