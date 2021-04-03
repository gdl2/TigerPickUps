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

        cursor.execute('DROP TABLE IF EXISTS activities')

        cursor.execute('CREATE TABLE activities ' +
            '(activity_counter SERIAL, name TEXT, place TEXT, starttime TEXT, endtime TEXT, description TEXT, gmaps_url TEXT)')

        connection.commit()

        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
