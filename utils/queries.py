from datetime import datetime, timedelta


def cmd_handler(cursor):
    while (True):
        print('Welcome to AwesTeam Queries! Type <exec> or <quit>')
        buf = input()
        if buf == 'exec':
            print('Which query to run?')
            buf = int(input())
            if buf < 1 or buf > 10:
                print('This query not implemented. Choose from 1 to 10')
            else:
                if buf == 1:
                    print('Type id of a customer')
                    id = int(input())
                    __query_1(cursor, id)
                if buf == 2:
                    print('Type date in format m/d/y. Only from 1/1/2018 to 12/31/2018')
                    s_date = input()
                    __query2(cursor, s_date)
                if buf == 3:
                    __query3(cursor)
                if buf == 4:
                    __query4(cursor)
                if buf == 5:
                    print('Type date in format m/d/y. Only from 1/1/2018 to 12/31/2018')
                    s_date = input()
                    __query5(cursor, s_date)
                if buf == 6:
                    __query6(cursor)
                if buf == 7:
                    __query7(cursor)
                if buf == 9:
                    __query9(cursor)
                if buf == 10:
                    __query10(cursor)
        elif buf == 'quit':
            break
        else:
            print("Wrong input. Available commands are <exec> and <quit>")


def __query_1(cursor, customer_id):
    cursor.execute("SELECT * FROM customers WHERE account_id=%s", (customer_id,))

    if (len(cursor.fetchall()) == 0):
        print("No customer with this id")
        return

    cursor.execute("""
        SELECT car_id, registration_number
        FROM cars, customers, orders
        WHERE orders.selected_car = cars.car_id AND
        cars.car_color = 'red' AND orders.customer = customers.account_id AND
        customers.account_id = %s AND cars.registration_number LIKE %s ESCAPE '';
    """, (customer_id, 'AN%'))

    result = cursor.fetchall()

    if (len(result) == 0):
        print("No cars for this customer. He/she is liar ¯\_(ツ)_/¯")

    for i in result:
        print("Possible cars:\n{} {}".format(i[0], i[1]))


def __query2(cursor, s_date):
    cursor.execute("""SELECT count(*) FROM charging_stations;""")
    print("Here is statistics from all {} stations for {}:".format(cursor.fetchone()[0], s_date))

    for i in range(24):
        n_date = datetime.strptime(s_date, '%m/%d/%Y') + timedelta(hours=i)
        cursor.execute("""SELECT sum(max - available) FROM station_plugs where date >= %s and date <= %s;""",
                       (n_date, n_date + timedelta(hours=1)))
        print("{}h-{}h: {}".format(i, i + 1, cursor.fetchone()[0]))


def __query3(cursor):
    print("Here is statistics for week 1 of 2018 year of percent of used cars:")
    cursor.execute("""select count(*) from cars;""")
    cars_number = cursor.fetchone()[0]

    curr_date = datetime(2018, 1, 8)
    for i in range(7):
        cursor.execute("""select count(*)
                    from (select selected_car
                    from orders
                    where creation_time >= %s and creation_time <= %s
                    group by selected_car) used_cars;""",
                       (curr_date, curr_date + timedelta(3)))
        print("Day {}:\nMorning: {}".format(i + 1, cursor.fetchone()[0] / cars_number * 100))

        curr_date += timedelta(hours=5)
        cursor.execute("""select count(*)
                    from (select selected_car
                    from orders
                    where creation_time >= %s and creation_time <= %s
                    group by selected_car) used_cars;""",
                       (curr_date, curr_date + timedelta(2)))
        print("Afternoon: {}".format(cursor.fetchone()[0] / cars_number * 100))

        curr_date += timedelta(hours=5)
        cursor.execute("""select count(*)
                    from (select selected_car
                    from orders
                    where creation_time >= %s and creation_time <= %s
                    group by selected_car) used_cars;""",
                       (curr_date, curr_date + timedelta(2)))
        print("Evening: {}\n".format(cursor.fetchone()[0] / cars_number * 100))

        curr_date += timedelta(hours=7)


def __query4(cursor):
    print('Id of lazy customer is 7. Searching for doubled payments for the last month (May 2018)...')

    # by the way, doubled row was intentionally added

    cursor.execute("""SELECT *
    FROM (SELECT *, count(*)
                        OVER
                          (PARTITION BY
                          source,
                          from_order
                          ) AS count
          FROM (select *
                from payments
                where date >= '2018-05-01'
                  and date < '2018-06-01'
                  and source = 7) lastMonthOrders) countedTable
    WHERE countedTable.count > 1;;""")

    result = cursor.fetchall()

    if (len(result) == 0):
        print("No doubled payments. Perhaps, customer wants to trick us. Send his lazy ass to bank")
    else:
        print("Found doubled payments! We're sorry...")
        for i in result:
            print("Customer charged for trip {} by {} at {}".format(i[4], i[1], i[2]))


def __query5(cursor, s_date):
    s_date = datetime.strptime(s_date, '%m/%d/%Y')
    cursor.execute("""select avg(distance)
        from orders
        where creation_time >= %s and end_time < %s;""",
                   (s_date, s_date + timedelta(days=1)))

    print("Average distance for {} is {} meters".format(s_date.date(), cursor.fetchone()[0]))

    cursor.execute("""select avg(end_time - creation_time)
    from orders
    where creation_time >= %s and end_time < %s;""",
                   (s_date, s_date + timedelta(days=1)))

    res = cursor.fetchone()

    print("Average trip duration for {} is {}".format(s_date.date(), res[0]))


def __query6(cursor):
    cursor.execute("""select address, count as travels
    from (SELECT destination, count
    FROM (SELECT *, count(*)
                        OVER
                          (PARTITION BY
                          destination
                          ) AS count
          FROM (select *
                from orders
                where date_part('hour', creation_time) >= %s
                  and date_part('hour', creation_time) <= %s) morningTravels) countedTable
    group by destination, count
    ORDER BY countedTable.count desc limit 3) topTable, addresses
    where topTable.destination = addresses.address_code;""", (7, 10))

    print("Top-3 destinations for morning:")
    for i in cursor.fetchall():
        print("{} travels to {}".format(i[1], i[0]))

    cursor.execute("""select address, count as travels
    from (SELECT destination, count
    FROM (SELECT *, count(*)
                        OVER
                          (PARTITION BY
                          destination
                          ) AS count
          FROM (select *
                from orders
                where date_part('hour', creation_time) >= %s
                  and date_part('hour', creation_time) <= %s) morningTravels) countedTable
    group by destination, count
    ORDER BY countedTable.count desc limit 3) topTable, addresses
    where topTable.destination = addresses.address_code;""", (12, 14))

    print("Top-3 destinations for afternoon:")
    for i in cursor.fetchall():
        print("{} travels to {}".format(i[1], i[0]))

    cursor.execute("""select address, count as travels
    from (SELECT destination, count
    FROM (SELECT *, count(*)
                        OVER
                          (PARTITION BY
                          destination
                          ) AS count
          FROM (select *
                from orders
                where date_part('hour', creation_time) >= %s
                  and date_part('hour', creation_time) <= %s) morningTravels) countedTable
    group by destination, count
    ORDER BY countedTable.count desc limit 3) topTable, addresses
    where topTable.destination = addresses.address_code;""", (17, 19))

    print("Top-3 destinations for evening:")
    for i in cursor.fetchall():
        print("{} travels to {}".format(i[1], i[0]))


def __query7(cursor):
    cursor.execute("SELECT count(*) FROM cars;")

    cars_num = cursor.fetchone()[0]

    to_decr = round(cars_num * 0.1)

    cursor.execute("""select car_color, car_model, registration_number, count
    from (SELECT selected_car, count
    FROM (SELECT *, count(*)
                        OVER
                          (PARTITION BY
                          selected_car
                          ) AS count
          FROM (select * from orders where creation_time >= '2018-01-01'
                                       and creation_time <= '2018-03-01')
                   lastMonthOrders) countedTable
    group by selected_car,count
    order by count
    limit %s) notUsedCars, cars
    where notUsedCars.selected_car = cars.car_id
    order by count;""", (to_decr,))

    print("Here are the least used {} (10%) cars of all {} cars for the last 3 months:".format(to_decr, cars_num))
    for i in cursor.fetchall():
        print("{} {} with number {} was used only {} times".format(i[0], i[1], i[2], i[3]))


def __query9(cursor):
    cursor.execute("SELECT count(*) from workshops;")
    workshops_num = cursor.fetchone()[0]

    for workshop in range(workshops_num):
        cursor.execute("SELECT detail_serial FROM details order by detail_serial;")
        details_ids = cursor.fetchall()
        for i,v in enumerate(details_ids):
            details_ids[i] = v[0]

        details_count = []

        for i, v in enumerate(details_ids):
            details_count.append(0)

        s_date = datetime(2018, 1, 1)
        for week in range(52):

            cursor.execute("""select detail, count(detail) as num from workshop_details
            where date >= %s and
              date <= %s and workshop = %s
            group by detail
            order by detail;

            """, (s_date, s_date + timedelta(weeks=1), workshop+1))

            result = cursor.fetchall()

            for i in result:
                details_count[details_ids.index(i[0])] += i[1]

            s_date+=timedelta(weeks=1, days=1)

        best_detail = details_ids[details_count.index(max(details_count))]
        cursor.execute("""SELECT detail_name FROM details where detail_serial=%s""", (best_detail,))

        print("Workshop {} most often needs {} ({} average per week).".format(workshop+1, cursor.fetchone()[0], round(max(details_count) / 52)))


def __query10(cursor):
    cursor.execute("""select car, sum(detail_cost * num) as total_cost
    from (select car, detail, count(*) as num
    from workshop_details
    group by car, detail
    order by car) cDet, details
    where cDet.detail = details.detail_serial
    group by car
    order by total_cost desc
    limit 1;""")

    cursor.execute("""SELECT car_color, car_model, registration_number FROM cars where car_id=%s;""",
                   (cursor.fetchone()[0],))

    res = cursor.fetchone()

    print("The highest expanses for repair were for the {} {} with number {}".format(res[0], res[1], res[2]))
