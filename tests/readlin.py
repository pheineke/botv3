with open("privacy_log.txt", 'r') as file:
    liste = [int(x) for x in file.readlines()]

with open("privacy_log.txt", 'w') as file:
    user_id = 386254372646158338

    if user_id in liste:
        liste.remove(user_id)
    for elem in liste:
        file.write(f"{elem}\n")