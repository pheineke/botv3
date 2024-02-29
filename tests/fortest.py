x = [1,2,3,4,5,False,6,False,False,7]

y = True

for elem in x if y else None:
    if type(elem) == bool:
        y = elem
    elif type(elem) == int:
        print(f"elem {elem} y {y}")
    else:
        print(f"y {y}")
        break

