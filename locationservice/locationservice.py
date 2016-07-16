import os
import http.client, urllib.parse
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
import locationservice.dbconns as dbconns

# create our little application :)
app = Flask(__name__)

app.run(host='0.0.0.0')

""" WTF IS THIS BLOCK """
# Load default config and override config from an environment variable
app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

# Is this needed?
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

""" end of WTF IS THIS BLOCK """

find_server_address = "ml.internalpositioning.com/"
# find_server_port = "80"
find_server_protocol = "https"
find_server_learn_route = "/learn"
find_server_track_route = "/track"

@app.route('/')
def index():
    return 'Hello, World'

@app.route('/venueReg', methods=['POST'])
def venue_registration():
    payload = request.form['data']

    venue = payload['venue']
    gps_lat = payload['gps_lat']
    gps_long = payload['gps_long']    

    #Insert into VENUE table
    if dbconns.put_venue_for_gps(gps_lat, gps_long, venue):
        # This is successful
        # TODO make the response
    else:
        #Unsuccessful

    return 'Venue registation'

@app.route('/learn', methods=['POST'])
def learn():
    if find_server_protocol == "http" :
        server_connection = http.client.HTTPConnection(find_server_address)
    elif find_server_protocol == "https" :
        server_connection = http.client.HTTPSConnection(find_server_address)

    # Parse payload
    payload = request.form['data']
    find_learn_payload = payload['find_payload']
    group = find_learn_payload['group']
    location = find_learn_payload['location']
    coupon_code = payload['coupon_code']

    # Make DB Entry (without duplicating)

    # Construct call for learn to public server
    server_connection.request("POST", find_server_learn_route, find_payload)
    server_response = server_connection.getresponse()
    print(server_response.status, server_response.read())
    server_connection.close()
    return 'Learning'

@app.route('/getVenueForGPS')
def get_venue_for_gps():
    payload = request.form['data']

    gps_lat = payload['gps_lat']
    gps_long = payload['gps_long']

    # Query VENUE Table
    venues = dbconns.get_venue_for_gps(gps_lat, gps_long)
    # TODO make the response

    # Return venue

    return 'Get Venue For GPS'

@app.route('/track')
def track():
    if find_server_protocol == "http" :
        server_connection = http.client.HTTPConnection(find_server_address)
    elif find_server_protocol == "https" :
        server_connection = http.client.HTTPSConnection(find_server_address)

    # Parse payload
    payload = request.form['data']
    find_track_payload = payload['find_payload']
    group = find_track_payload['group']

    # Construct call for track to public server
    server_connection.request("POST", find_server_track_route, find_track_payload)
    server_response = server_connection.getresponse()
    print(server_response.status, server_response.read())
    server_connection.close()

    # Get location from response

    # Query DB for coupon code and return
    return 'Tracking'


