#usertime.py
import modules.main.mensa.jsonhandler as jsh

from string import printable
import time
from table2ascii import table2ascii as t2a, PresetStyle

def mapuser(user, string):
        usermap = jsh.openjsonfile('usermapping','userdata.json')
        usermap[user] = string
        return "Dir wurde erfolgreich ein Alias erstellt."

def userread(user):
        localreaddata = jsh.openjsonfile('usercache','userdata.json')
        user = user.lower()

        try:
                userdata = str(localreaddata[user])
        except:
                return "nicht vorhanden."
        else:
                if userdata == 'false':
                        return 'False'
                
                userdatalen = len(userdata)
                hour, minute = userdata[:userdatalen//2], userdata[userdatalen//2:]

                return (hour + ':' + minute)

def userreadall():
        localreadall = jsh.openjsonfile('usercache','userdata.json')

        keys = [k for k, v in localreadall.items() if v == "false"]

        finallist = []
        i = 0

        for x in keys:
                del localreadall[x]
        if not localreadall:
                return "-> Keine.\n\n\n Bitch."
        else:
                for attribute, value in localreadall.items():

                        string = str(value)
                        firstpart, secondpart = string[:len(string)//2], string[len(string)//2:]
                        finallist.append([attribute, firstpart + ":" + secondpart])
                
                finallist = t2a(
                        header=["User", "Zeit"],
                        body=finallist,
                        style=PresetStyle.thin_compact)
                #print(finallist)
                return finallist


def userwrite(user, time):
        localuserwrite = jsh.openjsonfile('usercache', 'userdata.json')
        user = user.lower()
        localuserwrite[user] = time

        jsh.savefile(localuserwrite, 'usercache','userdata.json')

def userwriteuser(user0, user1):
        try:
                user1time = userread(user1)
                int(user1time)
        except:
                return "nicht gefunden."
        else:
                
                user0 = user0.lower()
                userwrite(user0, user1time[:2] + user1time[3:])
                return "als deine Zeit eingetragen." 

        


def userdelete(user):
        localuserdelete = jsh.openjsonfile('usercache.json')
        user = user.lower()

        try:
                del localuserdelete[user]
        except:
                return "Diesen User gibt es nicht."

        else:
                jsh.savefile(localuserdelete,'usercache.json')
                return "Der User wurde gelöscht."

def setuserconst(user):
        user = user.lower()
        userdata = jsh.openjsonfile('userdata.json','userconstants')
        userdata[user]= ""
        jsh.savefile(userdata, 'userdata.json','userconstants')

def deluserconst(user):
        userconstantsdelete = jsh.openjsonfile('userdata.json','userconstants')
        user = user.lower()

        try:
                del userconstantsdelete[user]
        except:
                return "Diesen User gibt es nicht."

        jsh.savefile(userconstantsdelete,'userconstants', 'userconstants')

def userreset():
    localuserconstants = jsh.openjsonfile('userconstants','userdata.json')
    data = jsh.openjsonfile('usercache','userdata.json')
    data2 = {}
    for key, value in data.items():
        if key in localuserconstants:
            data2[key] = value
    jsh.savefile(data2, 'usercache','userdata.json')

# TESTING:

if __name__ == "__main__":
        x = 5
        time.sleep(x)
        userwrite("n1ghtw1tch", 1300)
        time.sleep(x)
        userwrite("sees", 1300)
        time.sleep(x)
        setuserconst("n1ghtw1tch")
        time.sleep(x)
        userreset()
        time.sleep(x)
        userwrite("sees", 1300)
        time.sleep(x)
        deluserconst("n1ghtw1tch")
        time.sleep(x)
        userreset()
        '''
        sleep = 2
        userwrite("Joshie", 1340)
        print("Userwrite Joshie, 1340 DONE")
        time.sleep(sleep)
        userwrite("Moritz", 1350)
        print("Userwrite Joshie, 1350 DONE")
        time.sleep(sleep)
        userwrite("Joshie", "False")
        print("Userwrite Joshie, False DONE")
        time.sleep(sleep)
        print(userread("Joshie"))
        print("Userread Joshie DONE")
        time.sleep(sleep)
        print(userreadall())
        print("Userreadall DONE")
        time.sleep(sleep)
        print(userreadall())
        print("Userreadall DONE")
        time.sleep(sleep)
        userreset()
        print("Userreset DONE")
        time.sleep(sleep)
        userreadall()
        print("Userreadall DONE")
        '''