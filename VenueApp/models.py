#DrinkUp/VenueApp
import datetime
from urllib import urlencode
from django.db import models
from ApiApp.models import BaseModel
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save

from DrinkUp.BalancedHelper import BalancedPaymentsHelper

from geopy import geocoders
from facepy import GraphAPI

###################################################################

class Venue(models.Model):
	name = models.CharField(max_length=255)
	bp_merchant = models.CharField(max_length=255, blank=True)
	contact_email = models.EmailField(max_length=255)
	contact_number = models.BigIntegerField()
	street_address = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	postal_code = models.CharField(max_length=5)
	tax_id = models.CharField(max_length=9)
	icon = models.URLField(blank=True)
	facebook_id = models.CharField(max_length=255, blank=True, null=True)
	foursquare_id = models.CharField(max_length=255, blank=True, null=True)
	latitude = models.FloatField(editable=False)
	longitude = models.FloatField(editable=False)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
			#if not self.pk or not self.latitude or not self.longitude:
                        self.set_coords()
                                        #pass
			super(Venue, self).save(*args, **kwargs)

		# set coordinates
	def set_coords(self):
                        address = self.street_address +', '+self.city

                        domain = 'maps.googleapis.com'
                        params = {'address':address}

                        url = 'http://%(domain)s/maps/api/geocode/json?%(params)s&sensor=false' % ({'domain': domain, 'params': urlencode(params)})
                        
			g = geocoders.GoogleV3()
			place, (lat, lng) = g.geocode_url(url, False)[0]
			#place_area, (lat, lng) = g.geocode(self.postal_code)
			#place, (lat, lng) = g.geocode(self.street_address +', '+self.city)

			self.latitude = lat
			self.longitude = lng
		
###################################################################

WEEKDAYS = [
  (1, "Monday"),
  (2, "Tuesday"),
  (3, "Wednesday"),
  (4, "Thursday"),
  (5, "Friday"),
  (6, "Saturday"),
  (7, "Sunday"),
]

class VenueOpeningHours(BaseModel):
        venue = models.ForeignKey(Venue)
        weekday = models.IntegerField(choices=WEEKDAYS)
        open_hour = models.TimeField(default=datetime.time(0, 0, 0))
        close_hour = models.TimeField(default=datetime.time(0, 0, 0))
        happy_hour_start = models.TimeField(null=True, blank=True)
        happy_hour_end = models.TimeField(null=True, blank=True)
        closed = models.BooleanField(default=False)

        class Meta:
                unique_together = ('venue', 'weekday')

        def get_weekday_from_display(self):
                return WEEKDAYS[self.weekday_from]

        def get_weekday_to_display(self):
                return WEEKDAYS[self.weekday_to]

class VenueSpecialDays(BaseModel):
        venue = models.ForeignKey(Venue)
        holiday_date = models.DateField()
        closed = models.BooleanField(default=True)
        from_hour = models.TimeField(null=True, blank=True)
        to_hour = models.TimeField(null=True, blank=True)

        class Meta:
                unique_together = ('venue', 'holiday_date')

###################################################################

class VenueAdminUser(User):
	venue = models.ForeignKey(Venue)
	phone_number = models.BigIntegerField()
	dob = models.DateField()
	postal_code = models.CharField(max_length=5)
	street_address = models.CharField(max_length=255)
	
	objects = UserManager()
	
	def save(self, *args, **kwargs):
		if not self.venue.bp_merchant or len(self.venue.bp_merchant) == 0:
			self.createMerchant()
		super(VenueAdminUser, self).save(*args, **kwargs)

		# create a new merchant account
	def createMerchant(self):
		helper = BalancedPaymentsHelper()
		account = helper.setupNewMerchantAccount(merchant = self.venue, person = self)
		self.venue.bp_merchant = account.uri
		self.venue.save()
			
	class Meta:
		verbose_name = "Venue Admin User"

###################################################################
		
class BarAdminUser(User):
	venue = models.ForeignKey(Venue, null=True)
	bar = models.ForeignKey('BarApp.VenueBar')
	
	# Use UserManager to get the create_user method, etc.
	objects = UserManager()
	
	class Meta:
		verbose_name = "Venue Bar Admin User"

###################################################################

class VenueDrinkType(BaseModel):
	venue = models.ForeignKey(Venue)
	name = models.CharField(max_length=255)
	icon = models.URLField(blank=True)

	def __unicode__(self):
		return self.venue.name + ' ' + self.name
		
	class Meta:
		ordering = ['name']
		
###################################################################

class VenueBankAccount(BaseModel):

	Account_Type_Options = (('checking', 'checking'), ('savings','savings'))

	venue = models.ForeignKey(Venue)
	bank_name = models.CharField(max_length=255)
	routing_number = models.CharField(max_length=255)
	account_number = models.CharField(max_length=255)
	account_type = models.CharField(choices=Account_Type_Options, max_length=15)
	bp_uri = models.CharField(max_length=255, blank=True, null=True)
	
	def save(self, *args, **kwargs):
		if not self.bp_uri or len(self.bp_uri) == 0:
			self.addBankToMerchant()
		super(VenueBankAccount, self).save(*args, **kwargs)

	# create a new bank account, add to merchant account
	def addBankToMerchant(self):
		helper = BalancedPaymentsHelper()
		bank_account = helper.addMerchantBankAccount(merchant = self.venue, bank = self)
		self.bp_uri = bank_account.uri

        def __unicode__(self):
		return self.account_type + ' ' + self.account_number[-4:]
	
	class Meta:
		verbose_name = "Venue Bank Account"
		
###################################################################
