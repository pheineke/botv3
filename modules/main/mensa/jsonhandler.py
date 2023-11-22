#jsonhandler.py
import json

def openjsonfile(type, jsonfile):
        with open(jsonfile, 'r') as f:
                data = json.load(f)
                return data[type]
        
def savefile(data, type, file):
        with open(file, 'r') as f:
                jsondata = json.load(f)
                jsondata[type] = data
                with open(file, 'w') as f:
                        json.dump(jsondata,f)