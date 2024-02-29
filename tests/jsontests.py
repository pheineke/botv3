import json

x = {'hiimballat': ['13:00'], 'mew_g': ['13:00'], 'joshie_23': ['13:00'], 'n1ghtw1tch': ['11:30']}
y = ""
for key,value in x.items():
    y += f"{f"{key}":15} |  {str(value).replace("'","")}\n".replace("[","").replace("]","")

print(y)
