#-----------------------------------------------------------------------
# create.py
# Create working database for Tiger Pickups.
# Code adapted from COS 333 lectures by Bob Dondero.
#-----------------------------------------------------------------------

from os import path
from sys import argv, stderr, exit
from psycopg2 import connect

#-----------------------------------------------------------------------

def main(argv):

    if len(argv) != 1:
        print('Usage: python create.py', file=stderr)
        exit(1)

    try:
        connection = connect(
            host='localhost', port=5432, user='gabe', password='xxx',
            database='tigerpickupsdb')

        cursor = connection.cursor()

        #---------------------------------------------------------------

        cursor.execute('DROP TABLE IF EXISTS activities;')
        cursor.execute('DROP TABLE IF EXISTS users;')

        cursor.execute('CREATE TABLE activities ' +
            '(id SERIAL, host_net_id TEXT, host_name TEXT, title TEXT, type TEXT, \
            date TEXT, start_time TEXT, end_time TEXT, phone_number TEXT, \
            location TEXT, lat TEXT, lon TEXT, min_students TEXT, max_students TEXT, description TEXT);')

        cursor.execute('CREATE TABLE users ' +
            '(net_id INTEGER, name TEXT, residence TEXT, preferences BYTEA, current_location TEXT, attending_events BYTEA, created_events BYTEA);')

        connection.commit()

        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
