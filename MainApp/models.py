#DrinkUp / MainApp
from django.db import models
from ApiApp.models import BaseModel

from facepy import GraphAPI

class Venue(BaseModel):
	venue_owner = models.ForeignKey('VenueOwner')
	name = models.CharField(max_length=255)
	contact_email = models.EmailField(max_length=255)
	contact_number = models.PositiveIntegerField()
	address = models.TextField()
	icon = models.URLField(blank=True)
	facebook_id = models.CharField(max_length=255, blank=True, null=True)
	foursquare_id = models.CharField(max_length=255, blank=True, null=True)
		

class VenueOwner(BaseModel):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	phone = models.PositiveIntegerField()
		

class VenueBar(BaseModel):
	venue = models.ForeignKey(Venue)
	name = models.CharField(max_length=255)
	happyhour_start = models.DateTimeField()
	happyhour_end = models.DateTimeField()
	description = models.TextField(blank=True)
	is_active = models.BooleanField()
		

	def __unicode__(self):
		return self.name
		
	class Meta:
		ordering = ['name']
		

class Drink(BaseModel):
	bar = models.ForeignKey(VenueBar)
	drink_type = models.ForeignKey('DrinkType')
	name = models.CharField(max_length=255)
	price = models.DecimalField(decimal_places=2, max_digits=6)
	happyhour_price = models.DecimalField(decimal_places=2, max_digits=6)
	description = models.TextField(blank=True)

	def __unicode__(self):
		return self.name
		
	class Meta:
		ordering = ['name']
		
class DrinkType(BaseModel):
	type_name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.type_name
		
	class Meta:
		ordering = ['type_name']
		

class Order(BaseModel):
	bar = models.ForeignKey(VenueBar)
	appuser = models.ForeignKey('AppUser')
	total = models.DecimalField(decimal_places=2, max_digits=6)
	tax = models.DecimalField(decimal_places=2, max_digits=6)
	sub_total = models.DecimalField(decimal_places=2, max_digits=6)
	tip = models.DecimalField(decimal_places=2, max_digits=6)
	fees = models.DecimalField(decimal_places=2, max_digits=6)
	grand_total = models.DecimalField(decimal_places=2, max_digits=6)
	description = models.TextField(blank=True)

	def __unicode__(self):
		return str(self.appuser)
		
	class Meta:
		ordering = ['created']

class DrinkOrdered(models.Model):
	order = models.ForeignKey(Order)
	drink_name = models.CharField(max_length=255)
	quantity = models.PositiveIntegerField()
	unit_price = models.DecimalField(decimal_places=2, max_digits=6)
	drink_type = models.CharField(max_length=255)
	ordered_during_happyhour = models.BooleanField()

class AppUser(BaseModel):
	
	Gender_Options = (('Male', 'Male'), ('Female','Female'), ('Transgender','Transgender'))

	first_name = models.CharField(max_length=255, blank=True)
	last_name = models.CharField(max_length=255, blank=True)
	nickname = models.CharField(max_length=255) #bartender interface needs this
	email = models.EmailField(max_length=255)
	birthdate = models.DateField(blank=True)
	gender = models.CharField(choices=Gender_Options, max_length=15, blank=True)
	facebook_user = models.OneToOneField('FacebookAppUser', verbose_name='Facebook Profile', blank=True, null=True)
	foursquare_user = models.OneToOneField('FourSquareAppUser', verbose_name='Foursquare Profile', blank=True, null=True)
	password_salt = models.CharField(max_length=255)
	password_hash = models.CharField(max_length=255)
	is_active = models.BooleanField()
	
	def __unicode__(self):
		return self.email
		
	class Meta:
		ordering = ['email']


class FacebookAppUser(BaseModel):
	fb_uid = models.BigIntegerField(verbose_name = 'facebook id', unique=True)
	fb_email = models.EmailField(max_length=255, blank=True)
	oauth_token = models.OneToOneField('OAuthToken', verbose_name='OAuth token', blank=True, null=True)
		

class FourSquareAppUser(BaseModel):
	fs_uid = models.BigIntegerField(verbose_name = 'foursquare id', unique=True)
	fs_email = models.EmailField(max_length=255, blank=True)
	oauth_token = models.OneToOneField('OAuthToken', verbose_name='OAuth token', blank=True, null=True)
		

class OAuthToken(models.Model):
	"""
	Instances of the OAuthToken class are credentials used to query
	the Facebook API on behalf of a user.
	"""

	token = models.TextField()
	"""A string describing the OAuth token itself."""

	issued_at = models.DateTimeField()
	"""A ``datetime`` object describing when the token was issued."""

	expires_at = models.DateTimeField(null=True, blank=True)
	"""A ``datetime`` object describing when the token expires (or ``None`` if it doesn't)"""

	@property
	def expired(self):
		"""Determine whether the OAuth token has expired."""
		return self.expires_at < now() if self.expires_at else False

	@property
	def extended(self):
		"""Determine whether the OAuth token has been extended."""
		if self.expires_at:
			return self.expires_at - self.issued_at > timedelta(days=30)
		else:
			return False

	def extend_fb_token(self):
		"""Extend the OAuth token."""
		graph = GraphAPI()

		response = graph.get('oauth/access_token',
			client_id = FACEBOOK_APPLICATION_ID,
			client_secret = FACEBOOK_APPLICATION_SECRET_KEY,
			grant_type = 'fb_exchange_token',
			fb_exchange_token = self.token
		)

		components = parse_qs(response)

		self.token = components['access_token'][0]
		self.expires_at = now() + timedelta(seconds = int(components['expires'][0]))

		self.save()
	

