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
    all_lst_activities = db.get_activities()
    db.disconnect()

    html = render_template('index.html', mapbox_access_token = token, activities = all_lst_activities)
    response = make_response(html)
    return response

@app.route('/select_activities', methods=['GET'])
def select_activities():
    token = 'pk.eyJ1IjoiZ2xhbmlld3NraSIsImEiOiJja28weW13eHEwNWNwMnZzNTZyZzRrMDN4In0.P2-EylpYdzmCgdASgAKC5g'
    db = Database()
    db.connect()
    all_lst_activities = db.get_activities()
    db.disconnect()
    # id, host_net_id, host_name, title, type, date, start_time, end_time, phone_number, location, lat, lon, min_students, max_students, description
    chosen_lst_activities = []
    event_type = request.args.get('event_type')
    if (event_type is None) or (event_type == "all"):
        chosen_lst_activities = all_lst_activities
    else:
        for activity in all_lst_activities:
            if activity[4] == event_type:
                chosen_lst_activities.append(activity)

    results = []
    search = request.args.get('search')
    for activity in chosen_lst_activities:
        if search is None:
            results = chosen_lst_activities
        else:
            if search.lower() in activity[3].lower():
                results.append(activity)

    html = render_template('index.html', mapbox_access_token = token, activities = results)
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
    #host_net_id = request.args.get('host_net_id')
    host_name = request.args.get('host_name')
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

    if phone_number == '':
        phone_number = 'Na'
    if (min_students == "undefined") or (min_students == ''):
        min_students = 'Na'
    if (max_students == "undefined") or (max_students == ''):
        max_students = 'Na'
    if description == '':
        description = "Na"



    db = Database()
    db.connect()
    db.create_activity('', host_name, event_title, event_type, date, start_time, end_time, phone_number, loc, min_students, max_students, description)
    db.disconnect()

    return "Your event was successfully saved!"

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
