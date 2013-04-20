#DrinkUp/VenueApp
from django.db import models
from ApiApp.models import BaseModel
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save

from geopy import geocoders
from facepy import GraphAPI

###################################################################

class Venue(models.Model):
	name = models.CharField(max_length=255)
	contact_email = models.EmailField(max_length=255, blank=True)
	contact_number = models.PositiveIntegerField(blank=True, null=True)
	address = models.TextField()
	icon = models.URLField(blank=True)
	facebook_id = models.CharField(max_length=255, blank=True, null=True)
	foursquare_id = models.CharField(max_length=255, blank=True, null=True)
	latitude = models.FloatField(editable=False)
	longitude = models.FloatField(editable=False)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
                if not self.pk or self.latitude == 0 or not self.longitude == 0:
                        self.set_coords()
                super(Venue, self).save(*args, **kwargs)

        # set coordinates
        def set_coords(self):
            toFind = self.address
            g = geocoders.GoogleV3()

            place, (lat, lng) = g.geocode(toFind)

            self.latitude = lat
            self.longitude = lng
		
###################################################################

class VenueAdminUser(User):
	venue = models.ForeignKey(Venue, null=True)
	phone_number = models.PositiveIntegerField(blank=True, null=True)
	
	objects = UserManager()
	
	class Meta:
		verbose_name = "Venue Admin User"
		
###################################################################		
		
class BarAdminUser(User):
	venue = models.ForeignKey(Venue, null=True)
	bar = models.ForeignKey('BarApp.VenueBar', null=True)
	
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
		return self.name
		
	class Meta:
		ordering = ['name']