from django.utils.http import urlencode
from geopy.geocoders.base import Geocoder
import pinject
from VenueApp.binding_specs import VenueAppBindingSpec
import VenueApp

__author__ = 'Kinetic'

class GeoClass(object):
    def __init__(self, geocoder):
        self.geocoder = geocoder

class VenueAppProcessor(object):
    injector = pinject.new_object_graph(binding_specs=[VenueAppBindingSpec()])
    geocoder = injector.provide(GeoClass).geocoder

    @classmethod
    def setCoordinatesForVenue(cls, venue):
        assert isinstance(venue, VenueApp.models.Venue), "setCoordinatesForVenue requires a Venue instance"

        address = venue.street_address + ', ' + venue.city
        domain = 'maps.googleapis.com'
        params = {'address': address}
        url = 'http://%(domain)s/maps/api/geocode/json?%(params)s&sensor=false' % ({'domain': domain,
                                                                                    'params': urlencode(params)})
        place, (lat, lng) = cls.geocoder.geocode_url(url, False)[0]
        # place_area, (lat, lng) = g.geocode(self.postal_code)
        # place, (lat, lng) = g.geocode(self.street_address +', '+self.city)
        return lat, lng