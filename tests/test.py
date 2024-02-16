import random

biggerbase = ["A","B","C","D","E","F"]
base = 8
length = 12
a = [random.randint(0,base-1) for x in range(0,length)]
finallist = [x if x < 10 else biggerbase[(x%10)] for x in a ]
print(finallist)