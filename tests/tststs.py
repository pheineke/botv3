import time
import datetime
def print_progress_bar(progress):
    gif_frames = [
        ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
        ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
        ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
        ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
        ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
        ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
        ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
        ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
        ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
        ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
        ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️']
    ]

    for row in gif_frames:
        print(''.join(row[:progress]))

def check_time_difference(x):
    current_time = datetime.datetime.now()
    time_difference = current_time - x
    return time_difference.total_seconds() > 60

# Beispielverwendung:
previous_time = datetime.datetime.now()
progress = 0

while not check_time_difference(previous_time):
    print_progress_bar(progress)
    progress = (progress + 1) % 6  # In diesem Beispiel sind 5 Schritte erforderlich, um den Balken von links nach rechts zu füllen
    time.sleep(1)

print("Zeitdifferenz von mehr als 1 Minute festgestellt.")