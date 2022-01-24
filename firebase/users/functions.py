def checker(users, email):
    for i in users:
        if i['email'] == email:
            return i['username']

    return ""


def blogcheck(blog):
    if blog == None:
        return 1
    else:
        return len(blog)


