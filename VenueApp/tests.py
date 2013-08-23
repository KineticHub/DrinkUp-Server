"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import copy
from django.contrib.auth.models import User
from mock import MagicMock, Mock, patch
from django.test import TestCase
from VenueApp.models import Venue


class VenueAppTest(TestCase):

    USERNAME = "JSmith"
    EMAIL = "john.smith@example.com"
    PASSWORD = "jspassword"
    FAKE_BP_ACCOUNT = "/v1/customers/CU5iqmskN3o9gyBmuthvFaqP"

    def build_test_venue(self):
        return Venue(name='TestVenue', contact_email='venue.contact@example.com', contact_number=1234567890,
                     street_address='800 Drillfield Drive', city='Blacksburg', postal_code='20186',
                     timezone='UTC', tax_id=123456789)

    def test_add_geolocation_for_new_venue(self):
        """
        Test that the latitude and longitude of a venue are updated correctly
        when an address is given, more testing may be needed for international cases
        """

        EXPECTED_LATITUDE = 37.228272
        EXPECTED_LONGITUDE = -80.4231363

        venue = self.build_test_venue()
        venue.street_address = '800 Drillfield Drive'
        venue.city = 'Blacksburg'
        venue.postal_code = '20186'
        venue.save()

        self.assertEqual(venue.latitude, EXPECTED_LATITUDE, "latitude for venue does not match expected, got "
                                                            + str(venue.latitude) +
                                                            ", expected " + str(EXPECTED_LATITUDE))

        self.assertEqual(venue.longitude, EXPECTED_LONGITUDE, "longitude for venue does not match expected, got "
                                                            + str(venue.longitude) +
                                                            ", expected " + str(EXPECTED_LONGITUDE))