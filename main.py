#-----------------------------------------------------------------------
# index.py
# Displays activities in Princeton area.
# Code adapted from COS 333 lectures by Bob Dondero.
#-----------------------------------------------------------------------

from flask import Flask, render_template, make_response, url_for, redirect, request
from database import Database
import requests
from urllib.parse import urlencode, quote

#-------------------------------------------------------------------------------

app = Flask(__name__)

#-------------------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    token = 'pk.eyJ1IjoiZ2xhbmlld3NraSIsImEiOiJja28weW13eHEwNWNwMnZzNTZyZzRrMDN4In0.P2-EylpYdzmCgdASgAKC5g'
    db = Database()
    db.connect()
    lst_activities = db.get_activities()
    db.disconnect()

    html = render_template('index.html', mapbox_access_token = token, activities = lst_activities)
    response = make_response(html)
    return response

@app.route('/create', methods=['GET'])
def create():
    html = render_template('create.html')
    response = make_response(html)
    return response

@app.route('/form-party', methods=['GET'])
def form_party():
    html = render_template('form-party.html')
    response = make_response(html)
    return response

@app.route('/form-sports', methods=['GET'])
def form_sports():
    html = render_template('form-sports.html')
    response = make_response(html)
    return response

@app.route('/form-general', methods=['GET'])
def form_general():
    html = render_template('form-general.html')
    response = make_response(html)
    return response


@app.route('/about', methods=['GET'])
def about():
    html = render_template('about.html')
    response = make_response(html)
    return response


@app.route('/save_form', methods=['POST'])
def save_form():
    host_net_id = request.args.get('host_net_id')
    event_type = request.args.get('event_type')
    event_title = request.args.get('event_title')
    date = request.args.get('date')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    phone_number = request.args.get('phone_number')
    loc = request.args.get('loc')
    min_students = request.args.get('min_students')
    max_students = request.args.get('max_students')
    description = request.args.get('description')

    if (min_students == "undefined"):
        min_students = ''
    if (max_students == "undefined"):
        max_students = ''

    db = Database()
    db.connect()
    db.create_activity(host_net_id, "", event_title, event_type, date, start_time, end_time, phone_number, loc, min_students, max_students, description)
    db.disconnect()

    return "Your event was successfully saved!"



@app.route('/search', methods=['GET'])
def search():
    db = Database()
    db.connect()
    #user = request.args.get('user')
    name = request.args.get('name')
    place = request.args.get('place')
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    description = request.args.get('description')
    link = None
    if (place is not None):
        encoded_args = urlencode({'api': '1', 'destination': (place+ ", Princeton, NJ 08544")})
        link = ('https://www.google.com/maps/dir/?' + encoded_args)
    if (description is None) or (description.strip() == ''):
        description = ""
    if (name is not None) and (place is not None) and (starttime is not None) and (endtime is not None) and (description is not None):
        db.create_activity(name, place, starttime, endtime, description, link)
    activities =  db.get_activities()
    db.disconnect()
    html = render_template('search.html',
    activities = activities)

    response = make_response(html)
    return response

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
