#DrinkUp/UsersApp
from django.db import models
from ApiApp.models import BaseModel
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save

from DrinkUp.BalancedHelper import BalancedPaymentsHelper

###################################################################

class AppUser(models.Model):

	Gender_Options = (('male', 'male'), ('female','female'), ('transgender','transgender'))

	user = models.OneToOneField(User)
	bp_account = models.CharField(max_length=255, blank=True)
	profile_image = models.URLField(blank=True)
	birthdate = models.DateField(blank=True, null=True)
	gender = models.CharField(choices=Gender_Options, max_length=15, blank=True)
	facebook_user = models.OneToOneField('FacebookAppUser', verbose_name='Facebook Profile', blank=True, null=True)
	foursquare_user = models.OneToOneField('FourSquareAppUser', verbose_name='Foursquare Profile', blank=True, null=True)

	def save(self, *args, **kwargs):
		if not self.bp_account or len(self.bp_account) == 0:
			self.createAccount()
		super(AppUser, self).save(*args, **kwargs)

	# create a new buyer account
	def createAccount(self):
		helper = BalancedPaymentsHelper()
                new_account = helper.setupNewBuyerAccount(username=self.username, email_address=self.email)
                self.bp_account = new_account.uri

	def __unicode__(self):
		return self.user.username

###################################################################		

class FacebookAppUser(BaseModel):
	fb_uid = models.BigIntegerField(verbose_name = 'facebook id', unique=True)
	fb_email = models.EmailField(max_length=255, blank=True)
	oauth_token = models.OneToOneField('OAuthToken', verbose_name='OAuth token', blank=True, null=True)
	
	def __unicode__(self):
		return self.fb_email

###################################################################		

class FourSquareAppUser(BaseModel):
	fs_uid = models.BigIntegerField(verbose_name = 'foursquare id', unique=True)
	fs_email = models.EmailField(max_length=255, blank=True)
	oauth_token = models.OneToOneField('OAuthToken', verbose_name='OAuth token', blank=True, null=True)
		
###################################################################

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
