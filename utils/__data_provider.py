import itertools
from random import shuffle


def get_locations():
    gpsx = ["89.120", "17.67", "213.22", "32.2", "123.45", "12.90", "89.1", "16.98", "120.43", "53.72", "17.44"]
    gpsy = ["89.32", "78.11", "67.53", "16.98", "120.43", "53.72", "17.44", "12.48", "6.09", "67.90", "11.00"]
    tmp = list(itertools.product(gpsx, gpsy))
    shuffle(tmp)
    return tmp


def get_addresses():
    state = ["Ohio", "Oklahoma", "New York", "West Virginia", "Washington", "California", "Montana", "Wisconsin", "Illinois", "Alaska", "Nebraska"]
    city = ["New York", "Columbus", "Oklahoma City", "Olympia", "Charleston", "Nevada", "Salt Lake City", "Detroit"]
    street = ["Brooklyn", "Brighton Beach", "St. Patric", "Appalachian", "Beacon Street"]
    home = ["12", "1", "10", "22", "5", "14", "3", "123", "2", "3", "4", "5", "6", "7", "8", "9", "11"]
    tmp = [", ".join(i) for i in list(itertools.product(state, city, street, home))]
    shuffle(tmp)
    return tmp


def get_customers():
    username1 = ["lolka", "tinko", "hup", "popper", "reg", "nuker",
                 "dep", "unlink", "king", "sorreq", "opa", "34", "21",
                 "78", "42", "11", "3", "2001", "89", "2007", "fus", "ro", "dah"]

    username = [''.join(i) for i in list(itertools.combinations(username1, 3))]
    shuffle(username)

    name = ["John", "Derek", "Tony", "Bruce", "Alex", "Julio"]
    surname = ["Smith", "Wayne", "Stark", "Wakefield", "Sanderson", "Diaz", "Roberts"]
    # phone_num = ["17653490087", "17623440587", "15653221087", "10623499281", "12611490162"]

    phonenum1 = ["1763", "1032", "1004", "4031", "4046", "2392", "3408", "9832", "2169"]

    phone_num = [''.join(i) for i in list(itertools.combinations(phonenum1, 3))]
    shuffle(phone_num)

    email1 = ["lo", "re", "junk", "poop", "redem", "awes",
              "lel", "rat", "req", "king", "boom21", "54", "2007",
              ]
    email2 = [''.join(i) for i in list(itertools.combinations(email1, 2))]
    email3 = ["@edu.mit.com", "@gmail.com", "@bing.org"]
    email = [''.join(i) for i in list(itertools.product(email2, email3))]
    shuffle(email)

    # address = get_addresses()

    names = list(itertools.product(name, surname))
    shuffle(names)

    tmp = []
    counter = 0
    lim = len(names) - 1

    while (len(email) > 0 and len(username) > 0 and len(phone_num) > 0):
        tmp.append((username.pop(),
                    names[counter][0],
                    names[counter][1],
                    phone_num.pop(),
                    email.pop()))
        if(counter >= lim):
            counter = 0
        else:
            counter += 1

    shuffle(tmp)
    return tmp


def get_cars():
    regnum1 = ["AN", "BR", "CF", "EQ", "GH", "SS", "DO", "OP", "YE", "HU"]
    regnum2 = ["4390", "2130", "6297", "8630", "7612", "9952", "4501"]
    regnum3 = ["A", "B", "C", "D", "E", "F", "Q", "R", "S", "T", "U", "V"]

    regnum = [''.join(i) for i in list(itertools.product(regnum1, regnum2, regnum3))]
    shuffle(regnum)

    cmodel = ["Dodge", "Nissan", "Land Rover", "Porsche", "Lamborghini"]
    ccolor = ["red", "white", "blue", "purple", "cyan", "green"]

    cars = list(itertools.product(cmodel, ccolor))
    shuffle(cars)

    tmp = []
    counter = 0
    lim = len(cars) - 1

    while (len(regnum) > 0):
        tmp.append((
            regnum.pop(),
            cars[counter][0],
            cars[counter][1]
        ))
        if(counter >= lim):
            break
        counter += 1

    return tmp
