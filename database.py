#-----------------------------------------------------------------------
# database.py
# to connect to the database in cmd:
# psql -h localhost -p 5432 -U "username" -d cycdb
# Code adapted from COS 333 lectures
#-----------------------------------------------------------------------
from os import path
from sys import argv, stderr, exit
from psycopg2 import connect
from random import randint
#-----------------------------------------------------------------------

class Database:

    # constructor
    def __init__(self):
        self._connection = None

    # Connect to Database
    def connect(self):
        try:
            self._connection = connect(
                host='localhost', port=5432, user='gabe', password='xxx',
                database='tigerpickupsdb')
        except Exception as e:
            print(e, file = stderr)
            exit(1)

    # Disconnect from Database
    def disconnect(self):
        self._connection.close();

    # Get all activities stored inside Database
    def get_activities(self):
        cursor = self._connection.cursor()
        QUERY_STRING = "SELECT * FROM activities"
        cursor.execute(QUERY_STRING)
        lst_activities = cursor.fetchall()
        cursor.close()
        return lst_activities

    # Create activity
    def create_activity(self, name, place, starttime, endtime, description, gmaps_url):
        cursor = self._connection.cursor()
        QUERY_STRING = "INSERT INTO activities (activity_counter, name, place, starttime, endtime, description, gmaps_url) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)"
        cursor.execute(QUERY_STRING, [name, place, starttime, endtime, description, gmaps_url])
        self._connection.commit()
        cursor.close()

    def reset_db(self):
        cursor = self._connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS activities')
        cursor.execute('CREATE TABLE activities ' +
            '(activity_counter SERIAL, name TEXT, place TEXT, starttime TEXT, endtime TEXT, description TEXT)')
        cursor.close()

#-----------------------------------------------------------------------

if __name__ == "__main__":
    db = Database()
    db.connect()
    db.create_activity("Party", "1915 Hall", "Celebrate end of semester")
    print(db.get_activities())

    db.disconnect()
