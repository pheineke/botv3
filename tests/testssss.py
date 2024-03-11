from datetime import datetime
import re
def check_format(string):
    pattern = r'^[A-Z]-\d{3}$'
    if re.match(pattern, string):
        getint = string.split('-')
        return (0 < int(getint[1]) < 1000)
    else:
        return False

    
print(check_format("A-999"))

year = datetime.now().year
print(year)