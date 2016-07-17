from flask import Flask, request, jsonify
import locationservice.dbconns as dbconns
import requests

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY="development key",
    USERNAME="admin",
    PASSWORD="default"
))

FIND_server_address = "ml.internalpositioning.com"
# find_server_port = "80"

@app.route("/")
def index():
    """Default route"""
    return "Hello, World"

@app.route("/venueReg", methods=["POST"])
def venue_registration():
    """Register venue and return success/failure"""
    payload = request.get_json()
    venue = payload["venue"]
    print(venue)
    gps_lat = payload["gps_lat"]
    gps_long = payload["gps_long"]
    #Insert into VENUE table
    if dbconns.put_venue_for_gps(gps_lat, gps_long, venue):
        # This is successful
        response = jsonify({"success": True})
    else:
        response = jsonify({"success": False})

    return response

@app.route("/learn", methods=["POST"])
def learn():
    """Pass on FIND learn payload to public server.
    Extract group (Venue_GPS), coupon code and location
    and insert into DB.
    """

    # Parse payload
    payload = request.get_json()

    find_learn_payload = payload["find_payload"]

    group = find_learn_payload["group"]
    location = find_learn_payload["location"]
    group_list = group.split("_")
    venue = group_list[0]
    gps_lat = float(group_list[1])
    gps_long = float(group_list[2])

    coupon_code = payload["coupon_code"]
    print("coupon_code" + coupon_code)
    # Make DB Entry (without duplicating)
    dbconns.put_code_for_location(gps_lat, gps_long, venue, location, coupon_code)

    # Construct call for learn to public server
    r = requests.post("https://" + FIND_server_address + "/learn",
                      json=find_learn_payload)
    print(r.json())
    learn_response = r.json()
    return jsonify(learn_response)

@app.route("/getVenueForGPS", methods=["POST"])
def get_venue_for_gps():
    """Query VENUE table and return list of venues for GPS location"""
    payload = request.get_json()

    gps_lat = payload["gps_lat"]
    gps_long = payload["gps_long"]

    # Query VENUE Table
    venues = dbconns.get_gps_venues(gps_lat, gps_long)
    print(venues)
    response = jsonify(items=venues)

    # Return venue
    return response

@app.route("/track", methods=["POST"])
def track():
    """Pass on FIND track payload to public server.
    Extract group (Venue_GPS), and use response from public server
    to get location. Query BL using venue, GPS, location to return
    coupon code.
    """

    # Parse payload
    payload = request.get_json()
    find_track_payload = payload["find_payload"]
    group = find_track_payload["group"]

    # Construct call for track to public server
    r = requests.post("https://" + FIND_server_address + "/track",
                      json=find_track_payload)
    print(r.json())

    track_response = r.json()

    success = track_response["success"]
    if success == "true":
        # Get location from response
        group_list = group.split("_")
        venue = group_list[0]
        gps_lat = float(group_list[1])
        gps_long = float(group_list[2])
        location = track_response["location"]

        # Query DB for coupon code and return
        coupon_code = dbconns.get_code_for_location(gps_lat, gps_long, venue, location)
        response = jsonify(coupon_code=coupon_code,
                           location=location)
    else:
        response = jsonify(coupon_code="",
                           location="Not_found")
        
    return response

if __name__ == '__main__':
    app.run()