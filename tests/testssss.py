from datetime import datetime
import re
def check_format(string):
    pattern0 = r'^[A-Z]-\d{3}$'
    pattern1 = r'^[a-z]-\d{3}$'
    pattern2 = r'^[A-Z]\d{3}$'
    pattern3 = r'^[a-z]\d{3}$'
    if re.match(pattern0, string) or re.match(pattern0, string):
        getint = string.split('-')
        return (0 < int(getint[1]) < 1000)
    elif re.match(pattern2, string) or re.match(pattern3, string):
        getint = string[1:]
        print(getint)
    else:
        return False

print(check_format("a999"))
