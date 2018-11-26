import psycopg2 as sql
from utils import db_init as db
from utils import queries

db_name = 'dmd_ass'
connection = None

def create_tables():
    try:
        db.init_tables(connection)
        connection.commit()
        db.fill_tables(connection.cursor())
    except sql.Error as e:
        print("An error occured:", e.args[0])

def connect_to_db():
    global connection
    if (connection == None):
        try:
            connection = sql.connect("dbname={} user=postgres password=homepostgres host={} port={}".format(db_name, '138.197.156.69', '5432'))
        except sql.Error as e:
            print("An error occurred:", e.args[0])


if __name__ == "__main__":
    connect_to_db()
    #create_tables()
    queries.cmd_handler(connection.cursor())
    connection.commit()
    connection.close()
    print("Done")
