#DrinkUp/BarApp
from django.db import models
from ApiApp.models import BaseModel
from VenueApp.models import Venue, VenueDrinkType
from UsersApp.models import AppUser

from DrinkUp.BalancedHelper import BalancedPaymentsHelper
from DrinkUp.AirshipHelper import AirshipHelper

###################################################################

class VenueBar(BaseModel):
	venue = models.ForeignKey(Venue)
	name = models.CharField(max_length=255)
	happyhour_start = models.TimeField()
	happyhour_end = models.TimeField()
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.venue.name + ' ' + self.name
		
	class Meta:
		ordering = ['name']
		verbose_name = 'Bar'
		
###################################################################
		
class BarDrink(BaseModel):
	bar = models.ForeignKey(VenueBar)
	drink_type = models.ForeignKey('VenueApp.VenueDrinkType')
	name = models.CharField(max_length=255)
	price = models.DecimalField(decimal_places=2, max_digits=6)
	happyhour_price = models.DecimalField(decimal_places=2, max_digits=6)
	description = models.TextField(blank=True)

	def __unicode__(self):
		return self.bar.name + ' ' + self.name
		
	class Meta:
		ordering = ['name']
		
###################################################################

class BarOrder(BaseModel):

	Order_Status_Options = ((1, 'UNFILLED'), (2,'IN PROGRESS'), (3,'WAITING CUSTOMER'), (4,'ORDER COMPLETE'), (5,'ORDER CANCELLED'), (6,'ORDER NOT CLAIMED'))

	venue = models.ForeignKey(Venue)
	bar = models.ForeignKey(VenueBar)
	venue_name = models.CharField(max_length=255, blank=True)
	bp_transaction =  models.CharField(max_length=255, blank=True)
	appuser = models.ForeignKey('UsersApp.AppUser', related_name='appuser_owner')
	total = models.DecimalField(decimal_places=2, max_digits=6)
	tax = models.DecimalField(decimal_places=2, max_digits=6)
	sub_total = models.DecimalField(decimal_places=2, max_digits=6)
	tip = models.DecimalField(decimal_places=2, max_digits=6)
	fees = models.DecimalField(decimal_places=2, max_digits=6)
	grand_total = models.DecimalField(decimal_places=2, max_digits=6)
	current_status = models.IntegerField(max_length=1,choices=Order_Status_Options)
	description = models.TextField(blank=True)
	payment_processed = models.BooleanField()
	venue_payment_processed = models.BooleanField()

	def save(self, *args, **kwargs):
		if not self.bp_transaction or len(self.bp_transaction) == 0:
			#self.createHold()
			#self.description = 'hold created'
			pass
		if int(self.current_status) == 2:
						self.updateProgress()
		if int(self.current_status) == 3:
						self.updateReady()
		if int(self.current_status) == 4:
						if not self.payment_processed:
								#self.captureHold()
								self.processPayment()
								self.payment_processed = True
						self.description = 'payment processed'
		if int(self.current_status) == 5:
						#self.voidHold()
						#self.description = 'hold voided'
						self.description = 'order cancelled'
		super(BarOrder, self).save(*args, **kwargs)

		# create a new merchant account
	def createHold(self):
		helper = BalancedPaymentsHelper()
		hold = helper.createHoldForOrder(account = self.appuser, order = self)
		self.bp_transaction = hold.uri

	def updateProgress(self):
				pass
				#uahelper = AirshipHelper()
		#uahelper.pushMessageForUser(message='Your order is being made!', user=self.appuser.user, status=2)

	def updateReady(self):
		uahelper = AirshipHelper()
		uahelper.pushMessageForUser(message='Your order is ready! Go get it and DrinkUp!', user=self.appuser.user, status=3)

	def captureHold(self):
		helper = BalancedPaymentsHelper()
		hold = helper.captureHoldForOrder(order = self)

	def voidHold(self):
		helper = BalancedPaymentsHelper()
		hold = helper.voidHoldForOrder(order = self)
		uahelper = AirshipHelper()
		uahelper.pushMessageForUser(message='Your order was cancelled. No worries, we still like you!', user=self.appuser.user, status=5)
		
	def processPayment(self):
		helper = BalancedPaymentsHelper()
		self.bp_transaction = helper.debitBuyerCreditCard(account = self.appuser, order = self)
		

	def __unicode__(self):
		return str(self.appuser) + " " + str(self.current_status)
		
	class Meta:
		ordering = ['created']
		
###################################################################

class BarDrinkOrdered(models.Model):
	order = models.ForeignKey(BarOrder)
	drink_name = models.CharField(max_length=255)
	quantity = models.PositiveIntegerField()
	unit_price = models.DecimalField(decimal_places=2, max_digits=6)
	drink_type = models.CharField(max_length=255)
	ordered_during_happyhour = models.BooleanField()
