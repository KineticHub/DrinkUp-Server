from VenueApp.models import VenueOpeningHours

from datetime import datetime
import pytz

__author__ = 'Kinetic'


def convert_current_UTC_to_venue_local_datetime(venue):
    utc = datetime.utcnow()
    utc = utc.replace(tzinfo=pytz.utc)
    venue_timezone_time = utc.astimezone(venue.timezone)
    return venue_timezone_time


def convert_current_UTC_to_venue_local_time(venue):
    return convert_current_UTC_to_venue_local_datetime(venue).time()

# def determine_open_venues(venues):
# 	open_nearby_venues = []
# 	for venue in venues:
# 		weekday = convert_current_UTC_to_venue_local_datetime(venue).weekday()
# 		try:
# 			venue_weekday = VenueOpeningHours.objects.get(venue=venue, weekday=weekday)
# 		except VenueOpeningHours.DoesNotExist:
# 			continue
# 		if venue_weekday.open_hour < convert_current_UTC_to_venue_local_time(venue) < venue_weekday.close_hour \
# 			and not venue_weekday.closed:
# 			open_nearby_venues.append(venue)
#
# 	return open_nearby_venues

def determine_open_venues(venues):
    open_nearby_venues = []
    for venue in venues:
        weekday = convert_current_UTC_to_venue_local_datetime(venue).weekday()
        yesterday = convert_current_UTC_to_venue_local_datetime(venue).weekday() - 1
        try:
            venue_weekday = VenueOpeningHours.objects.get(venue=venue, weekday=weekday)
        except VenueOpeningHours.DoesNotExist:
            continue

        now = convert_current_UTC_to_venue_local_time(venue)
        if venue_weekday.open_hour < now < venue_weekday.close_hour \
            and not venue_weekday.closed:
            open_nearby_venues.append(venue)

        elif now < venue_weekday.open_hour:
            try:
                venue_weekday_yesterday = VenueOpeningHours.objects.get(venue=venue, weekday=yesterday)
            except VenueOpeningHours.DoesNotExist:
                continue

            if (venue_weekday_yesterday.open_hour > venue_weekday_yesterday.close_hour) \
                and (now < venue_weekday_yesterday.close_hour or now > venue_weekday_yesterday.open_hour) \
                and not venue_weekday_yesterday.closed:
                open_nearby_venues.append(venue)

    return open_nearby_venues