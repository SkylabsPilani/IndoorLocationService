import os
import http.client, urllib.parse
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, jsonify
import locationservice.dbconns as dbconns
import requests

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

find_server_address = "ml.internalpositioning.com"
# find_server_port = "80"
find_server_protocol = "https"
find_server_learn_route = "/learn"
find_server_track_route = "/track"

@app.route('/')
def index():
    return 'Hello, World'

@app.route('/venueReg', methods=['POST'])
def venue_registration():

    payload = request.form
    print(payload)

    venue = payload['venue']
    print(venue)
    gps_long = payload['gps_long']    
    #Insert into VENUE table
    if dbconns.put_venue_for_gps(gps_lat, gps_long, venue):
        # This is successful
        response = jsonify({"success": True})
    else:
        response = jsonify({"success": False})

    return response

@app.route('/learn', methods=['POST'])
def learn():

    # Parse payload
    payload = request.get_json()
    print(payload)

    find_learn_payload = payload['find_payload']

    group = find_learn_payload['group']
    location = find_learn_payload['location']

    coupon_code = payload['coupon_code']

    # Make DB Entry (without duplicating)

    # Construct call for learn to public server

    r = requests.post("https://" + find_server_address + find_server_learn_route, json=find_learn_payload)
    print(r.json())
   
    return jsonify(r.json())

@app.route('/getVenueForGPS', methods=['POST'])
def get_venue_for_gps():
    payload = request.get_json()

    gps_lat = payload['gps_lat']
    gps_long = payload['gps_long']

    # Query VENUE Table
    venues = dbconns.get_venue_for_gps(gps_lat, gps_long)
    response = jsonify(items=venues)

    # Return venue
    return response

@app.route('/track', methods=['POST'])
def track():
    if find_server_protocol == "http" :
        server_connection = http.client.HTTPConnection(find_server_address)
    elif find_server_protocol == "https" :
        server_connection = http.client.HTTPSConnection(find_server_address)

    # Parse payload
    payload = request.get_json()
    find_track_payload = payload['find_payload']
    group = find_track_payload['group']

    # Construct call for track to public server
    r = requests.post("https://" + find_server_address + find_server_track_route, json=find_track_payload)
    print(r.json())

    # Get location from response

    # Query DB for coupon code and return

    return jsonify(r.json())
