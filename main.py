#-----------------------------------------------------------------------
# index.py
# Displays activities in Princeton area.
# Code adapted from COS 333 lectures by Bob Dondero.
#-----------------------------------------------------------------------

from flask import Flask, render_template, make_response, url_for, redirect, request
from database import Database
from urllib.parse import urlencode

#-------------------------------------------------------------------------------

app = Flask(__name__)

#-------------------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
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
