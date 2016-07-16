import os
import tempfile
import pytest

from context import locationservice

learn_payload = {
    "find_payload": {"group":"deliciousdugong","username":"angelhack","password":"none","location":"vv","time":1468688047468,"wifi-fingerprint":[{"mac":"d4:68:4d:29:02:1c","rssi":-65},{"mac":"36:02:86:ba:0c:11","rssi":-55},{"mac":"fe:f8:ae:23:07:d5","rssi":-55},{"mac":"0c:d6:bd:54:09:89","rssi":-82},{"mac":"a4:ba:76:f2:18:cf","rssi":-86},{"mac":"0c:d6:bd:1d:fa:5a","rssi":-89},{"mac":"d4:68:4d:29:02:18","rssi":-63},{"mac":"c0:8a:de:76:4b:18","rssi":-67},{"mac":"c0:8a:de:36:4b:18","rssi":-68}]},
    "coupon_code": "ABCDE"
}

track_payload = {
    "find_payload": {"group":"deliciousdugong","username":"angelhack","password":"none","location":"tracking","time":1468688134334,"wifi-fingerprint":[{"mac":"d4:68:4d:29:02:1c","rssi":-68},{"mac":"36:02:86:ba:0c:11","rssi":-61},{"mac":"fe:f8:ae:23:07:d5","rssi":-68},{"mac":"0c:d6:bd:1d:fa:5a","rssi":-88},{"mac":"d4:68:4d:29:02:18","rssi":-62},{"mac":"c0:8a:de:76:4b:18","rssi":-69},{"mac":"c0:8a:de:36:4b:18","rssi":-69}]}
}

@pytest.fixture
def client(request):
    db_fd, locationservice.app.config['DATABASE'] = tempfile.mkstemp()
    locationservice.app.config['TESTING'] = True
    client = locationservice.app.test_client()
    # with locationservice.app.app_context():
    #     locationservice.init_db()

    def teardown():
        os.close(db_fd)
        # os.unlink(locationservice.app.config['DATABASE'])
    request.addfinalizer(teardown)
    return client

def learn(client, payload):
    return client.post('/learn', data=dict(
        data=payload
    ), follow_redirects=False)

def track(client, payload):
    return client.post('/track', data=dict(
        data=payload
    ), follow_redirects=False)

def test_learn_track(client):
    """Make sure learning and tracking works"""
    rv = learn(client, learn_payload)
    assert b'Learning was successful' in rv.data
    # rv = track(client, track_payload)
    # assert b'Tracking was successful' in rv.data
