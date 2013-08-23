from geopy import geocoders
import pinject
from DrinkUp.Helpers.BalancedHelper import BalancedPaymentsHelper

__author__ = 'Kinetic'

class VenueAppBindingSpec(pinject.BindingSpec):
    def configure(self, bind):
        bind('geocoder', to_class=geocoders.GoogleV3)