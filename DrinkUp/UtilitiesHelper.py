__author__ = 'Kinetic'
from datetime import datetime
import pytz

def convert_current_UTC_to_venue_local_datetime(venue):
	utc = datetime.utcnow()
	utc = utc.replace(tzinfo=pytz.utc)
	venue_timezone_time = utc.astimezone(venue.timezone)
	return venue_timezone_time

def convert_current_UTC_to_venue_local_time(venue):
	return convert_current_UTC_to_venue_local_datetime(venue).time()