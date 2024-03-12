from discord import Embed
from tabulate import tabulate

data = {
    'greyBox_1': {
        'IP-Adresse:': '131.246.227.145',
        'Panelport:': '68-1V1.14-1',
        'Switch:': 'buntes-sw4',
        'Wohnheim:': 'Buntes',
        'Zimmer:': 'B-112'
    },
    'greyBox_2': {
        'Duplex:': 'unknown',
        'Link:': 'up',
        'Port:': 'Fa0/1',
        'Speed:': 'unknown',
        'Status:': 'enabled'
    }
}

# Convert dictionary to list of lists
table = [[f"{key}: {value}" for key, value in data['greyBox_1'].items()],
         [f"{key}: {value}" for key, value in data['greyBox_2'].items()]]

# Add empty strings to align columns
max_length = max(len(box) for box in table)
for box in table:
    box.extend([''] * (max_length - len(box)))

# Transpose the table
table_transposed = list(zip(*table))

# Format the table
table_formatted = tabulate(table_transposed, tablefmt='grid')

# Create a Discord Embed
embed = Embed(title="Dictionary as 2 by 2 column table")
embed.add_field(name="greyBox_1", value="```" + table_formatted[:len(table_formatted)//2] + "```", inline=True)
embed.add_field(name="greyBox_2", value="```" + table_formatted[len(table_formatted)//2:] + "```", inline=True)

# Print or return the Discord Embed
print(embed.to_dict())  # Print Embed as dictionary for Discord
