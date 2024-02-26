import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


datum0 = "2024-02-26"
datum1 = "2024-02-26"

# Laden der Daten aus der Datei
data = np.loadtxt('data.txt', delimiter=',',dtype=str)


values = [row[2] == 'True' for row in data]
dates = [datetime.strptime(row[0] + ' ' + row[1], '%Y-%m-%d %H:%M') for row in data]
date_values = [[dates[i], values[i]] for i in range(len(dates))]

if not(datum0 and datum1):
    filtered_entries = date_values
elif datum0 and not datum1:
    filtered_entries = [entry for entry in date_values if datum0 in str(entry[0])]
elif datum0 and datum1:
    filtered_entries = [entry for entry in date_values if datum0 in str(entry[0]) or datum1 in str(entry[0])]
else:
    filtered_entries = date_values


plot_dates = [str(x[0]) for x in filtered_entries]
plot_values = [str(x[1]) for x in filtered_entries]
# Erstellen des Diagramms
plt.figure(figsize=(20, 2))
plt.plot(plot_dates, values, marker='o', linestyle='-', color='b')
plt.xlabel('Date and Time')
plt.ylabel('Value')
plt.title('Boolean Data over Time')
plt.yticks([0, 1], ['False', 'True'])
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("plot-door.png")
