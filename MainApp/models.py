#DrinkUp / MainApp
from django.db import models
from ApiApp.models import BaseModel

from facepy import GraphAPI

class Bar(BaseModel):
	email = models.EmailField(max_length=255)
	name = models.CharField(max_length=255)
	icon = models.URLField()
	lattitude = models.FloatField()
	longitude = models.FloatField()
	zipcode = models.PositiveIntegerField()

	def __unicode__(self):
		return self.name
		
	class Meta:
		ordering = ['name']
		

class AppUser(BaseModel):
	
	Gender_Options = (('Male', 'Male'), ('Female','Female'), ('Transgender','Transgender'))

	first_name = models.CharField(max_length=255, blank=True)
	last_name = models.CharField(max_length=255, blank=True)
	nickname = models.CharField(max_length=255, blank=True)
	email = models.EmailField(max_length=255)
	birthdate = models.DateField(blank=True)
	gender = models.CharField(choices=Gender_Options, max_length=15, blank=True)
	
	facebook_user = models.OneToOneField('FacebookAppUser', verbose_name='Facebook Profile', blank=True, null=True)
	
	def __unicode__(self):
		return self.nickname
		
	class Meta:
		ordering = ['nickname']


class FacebookAppUser(BaseModel):
	fb_uid = models.BigIntegerField(verbose_name = 'facebook id', unique=True)
	fb_email = models.EmailField(max_length=255, blank=True, null=True)
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

	def extend(self):
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

class DrinkType(BaseModel):
	bar = models.ForeignKey(Bar)
	type_name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.type_name
		
	class Meta:
		ordering = ['type_name']
	
class Drink(BaseModel):
	bar = models.ForeignKey(Bar)
	drink_type = models.ForeignKey(DrinkType)
	name = models.CharField(max_length=200)
	price = models.DecimalField(decimal_places=2, max_digits=6)

	def __unicode__(self):
		return self.name
		
	class Meta:
		ordering = ['name']
	
class Order(BaseModel):
	bar = models.ForeignKey(Bar)
	appuser = models.ForeignKey(AppUser)
	datetime = models.DateTimeField(auto_now_add=True)
	total = models.DecimalField(decimal_places=2, max_digits=6)
	tax = models.DecimalField(decimal_places=2, max_digits=6)
	sub_total = models.DecimalField(decimal_places=2, max_digits=6)
	tip = models.DecimalField(decimal_places=2, max_digits=6)
	grand_total = models.DecimalField(decimal_places=2, max_digits=6)
	description = models.TextField(blank=True)

	def __unicode__(self):
		return str(self.appuser)
		
	class Meta:
		ordering = ['datetime']

class DrinkOrdered(BaseModel):
	order = models.ForeignKey(Order)
	drink = models.ForeignKey(Drink)
	quantity = models.PositiveIntegerField()

