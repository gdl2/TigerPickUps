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
import json
from geopy.geocoders import Nominatim
from urllib.parse import urlencode, quote
#-----------------------------------------------------------------------

class Database:

    # constructor
    def __init__(self):
        self._connection = None

    # Connect to Database
    def connect(self):
        try:
            ############ Needed for Heroku deployment
            DATABASE_URL = environ['DATABASE_URL']
            self._connection = connect(
                DATABASE_URL, sslmode='require')

            ############# Needed for local deployment
            # self._connection = connect(
            #     host='localhost', port=5432, user='gabe', password='xxx',
            #     database='tigerpickupsdb')
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

        activities_list = []
        row = cursor.fetchone()
        while row is not None:
            activities_list.append(list(row))
            row = cursor.fetchone()
        cursor.close()

        return activities_list

    # Get all activities stored inside Database
    def get_locations(self):
        cursor = self._connection.cursor()
        QUERY_STRING = "SELECT location FROM activities"
        cursor.execute(QUERY_STRING)

        location_list = []
        row = cursor.fetchone()
        while row is not None:
            location_list.append(row[0])
            row = cursor.fetchone()
        cursor.close()

        return location_list

    # Create activity
    def create_activity(self, host_net_id, host_name, title, type, date, start_time, end_time, phone_number, location, min_students, max_students, description):
        cursor = self._connection.cursor()
        #token = 'pk.eyJ1IjoiZ2xhbmlld3NraSIsImEiOiJja28weW13eHEwNWNwMnZzNTZyZzRrMDN4In0.P2-EylpYdzmCgdASgAKC5g'
        #parsed_location = quote(location+", Princeton, NJ 08544")
        #response = requests.get("https://api.mapbox.com/geocoding/v5/mapbox.places/"+parsed_location+".json?access_token="+token)
        #dict = json.loads(response.text)
        #lon, lat = dict['features'][0]['center']
        geolocator = Nominatim(user_agent="tiger-pickups")
        place = geolocator.geocode(location+", Princeton, NJ 08544")
        lat, lon = place.latitude, place.longitude
        QUERY_STRING = "INSERT INTO activities (id, host_net_id, host_name, title, type, date, start_time, end_time, phone_number, location, lat, lon, min_students, max_students, description) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(QUERY_STRING, [host_net_id, host_name, title, type, date, start_time, end_time, phone_number, location, lat, lon, min_students, max_students, description])
        self._connection.commit()
        cursor.close()

    # Create user
    def create_user(self, net_id, name, residence, preferences, current_location, attending_events, created_events):
        cursor = self._connection.cursor()
        QUERY_STRING = "INSERT INTO users (net_id, name, residence, preferences, current_location, attending_events, created_events) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(QUERY_STRING, [net_id, name, residence, repr(preferences), current_location, repr(attending_events), repr(created_events)])
        self._connection.commit()
        cursor.close()

    def reset_db(self):
        cursor = self._connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS activities;')
        cursor.execute('DROP TABLE IF EXISTS users;')

        cursor.execute('CREATE TABLE activities ' +
            '(id SERIAL, host_net_id TEXT, host_name TEXT, title TEXT, type TEXT, \
            date TEXT, start_time TEXT, end_time TEXT, phone_number TEXT, \
            location TEXT, lat TEXT, lon TEXT, min_students TEXT, max_students TEXT, description TEXT);')

        cursor.execute('CREATE TABLE users ' +
            '(net_id INTEGER, name TEXT, residence TEXT, preferences BYTEA, current_location TEXT, attending_events BYTEA, created_events BYTEA);')
        cursor.close()


#-----------------------------------------------------------------------

if __name__ == "__main__":
    db = Database()
    db.connect()
    print(db.get_activities())
    print("\n\n")
    lst_locations = db.get_locations()
    print(lst_locations)
    db.disconnect()
