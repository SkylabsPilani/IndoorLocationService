import boto3
import json

dynamodb = boto3.resource('dynamodb')
gps_venue_table = dynamodb.Table('GPSVenues')
gps_venue_table_key = 'GPSCoordinates'
gps_venue_table_venue_key = 'Venues'

def get_gps_venues(gps_coordinates):
    gps_dict = {gps_venue_table_key:gps_coordinates}
    response = gps_venue_table.get_item(Key=gps_dict)
    try:
        venues = json.loads(json.dumps(response['Item']))['Venues']
    except KeyError:
        venues = None

    return venues

def put_venue_for_gps(gps_coordinates, venue):
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
    else :
        return False
