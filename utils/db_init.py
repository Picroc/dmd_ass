from utils import __data_provider as provider
from random import randint, shuffle, random
from utils import rand_time
from datetime import datetime, timedelta

db_file = "utils/db_setup.sql"
date_format = '%m/%d/%Y %I:%M %p'


def init_tables(connector):
    cursor = connector.cursor()
    for i in __get_querries():
        if (len(i) <= 0):
            continue
        cursor.execute(i)
    print("Tables have been created.")


def __get_querries():
    res = []
    with open(db_file) as file:
        res = file.read().split(";")
    return res


def fill_tables(cursor):
    __generate_location(cursor)
    __fill_cars(cursor)
    __fill_activity(cursor)
    __fill_charging_stations(cursor)
    __fill_providers(cursor)
    __fill_workshops(cursor)


locations = None
customers = None
addresses = None
cars = None


def __generate_location(cursor):
    global locations

    if (locations == None):
        locations = provider.get_locations()

    if (len(locations) <= 0):
        locations = None
        return __generate_location(cursor)
    else:
        cursor.execute("""INSERT INTO Locations(gpsx, gpsy)
                            VALUES (%s,%s) returning location_id;""",
                       locations.pop())

    id = cursor.fetchone()[0]

    global addresses
    if (addresses == None):
        addresses = provider.get_addresses()

    if (len(addresses) <= 0):
        addresses = provider.get_addresses()

    cursor.execute("""INSERT INTO Addresses(address_code, address)
                        VALUES (%s, %s)""", [id, addresses.pop()])

    return id


def __get_locations_set(cursor):
    cursor.execute("""SELECT location_id FROM locations;""")

    return cursor.fetchall()


def __generate_new_customer(cursor):
    global customers

    if (customers == None):
        customers = provider.get_customers()

    if (len(customers) <= 0):
        customers = None
        __generate_new_customer(cursor)

    id = __generate_location(cursor)

    customer = customers.pop()

    cursor.execute("""INSERT INTO customers(
        account_username,
        customer_name,
        customer_surname,
        phone_number,
        email,
        location) 
    VALUES (%s, %s, %s, %s, %s, %s) returning account_id""",
                   (customer[0], customer[1], customer[2], customer[3], customer[4], id))

    id = cursor.fetchone()[0]

    return id


def __fill_providers(cursor):
    global customers
    lim = 10

    for i in range(lim):
        if (len(customers) <= 0):
            customers = provider.get_customers()
        id = __generate_location(cursor)
        det_provider = customers.pop()
        cursor.execute("""INSERT INTO detail_provider(name, surname, phone, email, address) VALUES 
        (%s, %s, %s, %s, %s)""", (det_provider[1], det_provider[2], det_provider[3], det_provider[4], id))


def __fill_charging_stations(cursor):
    lim = 3

    station_ids = []
    cursor.execute("SELECT plug_serial FROM plugs")
    plug_ids = cursor.fetchall()

    for i in range(lim):
        id = __generate_location(cursor)
        cursor.execute("""INSERT INTO charging_stations(location, charging_cost) 
        VALUES (%s, %s) returning charging_station_id""", [id, randint(2, 10)])

        station_ids.append(cursor.fetchone()[0])

    num_of_entries = 24
    days = 30
    for d in range(days):
        for j in range(num_of_entries):
            print("Day {} hour {}".format(d, j))
            plug_date = datetime.strptime("1/1/2018 12:00 AM", date_format) + timedelta(days=d, hours=j)
            # plug_id = plug_ids[randint(0, len(plug_ids) - 1)][0]
            for i in station_ids:
                for plug_id in plug_ids:
                    cursor.execute(
                        """INSERT INTO station_plugs(station, plug, available, max, date) VALUES (%s, %s, %s, %s, %s)""",
                        (i, plug_id[0], randint(8, 10), randint(10, 12), plug_date))


def __fill_workshops(cursor):
    lim = 2

    workshop_ids = []
    cursor.execute("SELECT detail_serial FROM details")
    detail_ids = cursor.fetchall()
    cursor.execute("SELECT provider_id FROM detail_provider")
    provider_ids = cursor.fetchall()

    for i in range(lim):
        id = __generate_location(cursor)
        cursor.execute("""INSERT INTO workshops(location) 
        VALUES (%s) returning workshop_id""", [id])

        workshop_ids.append(cursor.fetchone()[0])

    #used_ids = []
    cars_ids = cars.copy()
    shuffle(cars_ids)

    for d in range(30*12):
        for i in workshop_ids:
            for j in range(randint(5, 20)):
                det_id = detail_ids[randint(0, len(detail_ids) - 1)][0]

                if(len(cars_ids) <= 0):
                    cars_ids = cars.copy()
                    shuffle(cars_ids)

                s_date = datetime.strptime(rand_time.randomDate("1/1/2018 1:00 AM", "12/31/2018 10:00 PM", random()), date_format)
                cursor.execute("""INSERT INTO workshop_details(workshop, detail, provider, car, date) VALUES (%s, %s, %s, %s, %s)""",
                               (i, det_id, provider_ids[randint(0, len(provider_ids) - 1)][0], cars_ids.pop(), s_date))
                #used_ids.append(det_id)


def __fill_cars(cursor):
    global cars
    cars = []

    cursor.execute("SELECT plug_serial FROM plugs")
    plugs = cursor.fetchall()

    generated = provider.get_cars()
    for car in generated:
        id = __generate_location(cursor)
        cursor.execute("""INSERT INTO cars
        (registration_number, car_model, car_color, location, charge_level, damage_level, plug_type) 
        values (%s, %s, %s, %s, %s, %s, %s) returning car_id""",
                       (car[0], car[1], car[2], id, randint(20, 100), randint(40, 100), plugs[randint(0, 3)][0]))

        cars.append(cursor.fetchone()[0])


def __fill_activity(cursor):
    orders_count = 3000

    cars_list = cars.copy()
    loc_list = __get_locations_set(cursor)
    shuffle(cars_list)
    shuffle(loc_list)

    for i in range(orders_count):
        if (len(cars_list) <= 0):
            cars_list = cars.copy()
            shuffle(cars_list)

        if( len(loc_list) <= 2):
            loc_list = __get_locations_set(cursor)
            shuffle(loc_list)

        customer_id = __generate_new_customer(cursor)

        dep = loc_list.pop()[0]
        dest = loc_list.pop()[0]

        s_time = rand_time.randomDate("1/1/2018 1:00 AM", "12/31/2018 10:00 PM", random())
        mid_time = datetime.strptime(s_time, date_format) + timedelta(hours=4)
        e_time = rand_time.randomDate(s_time, mid_time.strftime(date_format), random())

        while dep == dest:
            dest = __generate_location(cursor)

        cursor.execute("""INSERT INTO Orders(departure, destination, selected_car, creation_time, end_time, customer, distance) 
        VALUES (%s, %s, %s, %s, %s, %s, %s) returning order_id""",
                       (dep, dest, cars_list.pop(), datetime.strptime(s_time, date_format),
                        datetime.strptime(e_time, date_format), customer_id,
                        randint(200, 10000)))

        cursor.execute("""INSERT INTO payments(amount, date, source, from_order) VALUES (%s, %s, %s, %s)""",
                       (randint(13, 500), datetime.strptime(e_time, date_format), customer_id,
                        cursor.fetchone()[0]))
