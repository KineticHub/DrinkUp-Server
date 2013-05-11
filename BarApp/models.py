#DrinkUp/BarApp
from django.db import models
from ApiApp.models import BaseModel
from VenueApp.models import Venue, VenueDrinkType
from UsersApp.models import AppUser

from DrinkUp.BalancedHelper import BalancedPaymentsHelper

###################################################################

class VenueBar(BaseModel):
	venue = models.ForeignKey(Venue)
	name = models.CharField(max_length=255)
	happyhour_start = models.TimeField()
	happyhour_end = models.TimeField()
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.name
		
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
		return self.name
		
	class Meta:
		ordering = ['name']
		
###################################################################

class BarOrder(BaseModel):

	Order_Status_Options = ((1, 'UNFILLED'), (2,'IN PROGRESS'), (3,'WAITING CUSTOMER'), (4,'ORDER COMPLETE'), (5,'ORDER CANCELLED'), (6,'ORDER NOT CLAIMED'))

	bar = models.ForeignKey(VenueBar)
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

	def save(self, *args, **kwargs):
		if not self.bp_transaction or len(self.bp_transaction) == 0:
			self.createHold()
		if self.current_status == 4:
                        self.captureHold()
		if self.current_status == 5:
                        self.voidHold()
		super(BarOrder, self).save(*args, **kwargs)

        # create a new merchant account
	def createHold(self):
		helper = BalancedPaymentsHelper()
		hold = helper.createHoldForOrder(account = self.appuser, order = self)
		self.bp_transaction = hold.uri

	def captureHold(self):
		helper = BalancedPaymentsHelper()
		hold = helper.captureHoldForOrder(order = self)

	def voidHold(self):
		helper = BalancedPaymentsHelper()
		hold = helper.voidHoldForOrder(order = self)

	def __unicode__(self):
		return str(self.appuser)
		
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
