import matplotlib.pyplot as plt
import numpy as np

# Zeitstempel in einem Array
timestamps = ["2024-02-28 10:00:00", "2024-02-28 11:00:00", "2024-02-28 12:00:00", "2024-02-28 12:00:00"]

# Umwandlung der Zeitstempel in datetime-Objekte
timestamps = [np.datetime64(ts) for ts in timestamps]

# Erstellung der Werte, die von 0 bis 2 über den Zeitraum ansteigen
values = [0,1,0,2]

# Plotting
plt.figure(figsize=(10, 6))

plt.plot(timestamps, values, label='Wert von 0 bis 2 über Zeit')

plt.xlabel('Zeitstempel')
plt.ylabel('Wert')
plt.title('Linie mit Werten von 0 bis 2 über Zeit')
plt.legend()

plt.show()
