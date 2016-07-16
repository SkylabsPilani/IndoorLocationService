import os
import http.client, urllib.parse
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash


# create our little application :)
app = Flask(__name__)

""" WTF IS THIS BLOCK """
# Load default config and override config from an environment variable
app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
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

@app.route('/learn', methods=['POST'])
def learn():
    if find_server_protocol == "http" :
        # server_connection = http.client.HTTPConnection(find_server_address, find_server_port)
        server_connection = http.client.HTTPConnection(find_server_address)
    elif find_server_protocol == "https" :
        # server_connection = http.client.HTTPSConnection(find_server_address, find_server_port)
        server_connection = http.client.HTTPSConnection(find_server_address)

    fingerprint = request.form['fingerprint']

    params = urllib.parse.urlencode({'dataType': "json", 'data': fingerprint})

    server_connection.request("POST", find_server_learn_route, params)
    server_response = server_connection.getresponse()
    print(server_response.status, server_response.read())
    server_connection.close()


    return 'Hello, World'

"""@app.route('/track')
def train():"""

