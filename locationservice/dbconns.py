import boto3
import json

dynamodb = boto3.resource('dynamodb')
gps_venue_table = dynamodb.Table('GPSVenues')
gps_venue_table_key = 'GPSCoordinates'
gps_venue_table_venue_key = 'Venues'


def __normalize_coordinates__(gps_lat, gps_lon):
    return str(int(float(gps_lat))) + str(int(float(gps_lon)))


def __get_gps_venues__(gps_coordinates):
    gps_dict = {gps_venue_table_key:gps_coordinates}
    response = gps_venue_table.get_item(Key=gps_dict)
    try:
        venues = json.loads(json.dumps(response['Item']))['Venues']
    except KeyError:
        venues = None

    return venues


def __put_venue_for_gps__(gps_coordinates, venue):
    venues = get_gps_venues(gps_coordinates)
    if venues is None:
        venues = [venue]
    else:
        if venue not in venues:
            venues.append(venue)
        else:
            return True
    gps_dict = {gps_venue_table_key: gps_coordinates, gps_venue_table_venue_key: venues}
    if gps_venue_table.put_item(Item=gps_dict)['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def get_gps_venues(gps_lat, gps_lon):
    return __get_gps_venues__(__normalize_coordinates__(gps_lat, gps_lon))


def put_venue_for_gps(gps_lat, gps_lon, venue):
    return __put_venue_for_gps__(__normalize_coordinates__(gps_lat, gps_lon), venue)

