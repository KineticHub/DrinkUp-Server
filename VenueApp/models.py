#DrinkUp/VenueApp
import datetime
from urllib import urlencode

from django.db import models
from django.contrib.auth.models import User, UserManager
from timezone_field import TimeZoneField

from ApiApp.models import BaseModel
from DrinkUp.Helpers.BalancedHelper import BalancedPaymentsHelper
from VenueApp.processor import VenueAppProcessor


###################################################################



class Venue(models.Model):
    venue_app_processor = VenueAppProcessor()

    name = models.CharField(max_length=255)
    bp_merchant = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(max_length=255)
    contact_number = models.BigIntegerField()
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=5)
    timezone = TimeZoneField()
    tax_id = models.CharField(max_length=9)
    icon = models.URLField(blank=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    foursquare_id = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(editable=False)
    longitude = models.FloatField(editable=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.latitude, self.longitude = self.venue_app_processor.setCoordinatesForVenue(self)
        super(Venue, self).save(*args, **kwargs)

###################################################################

WEEKDAYS = [
  (0, "Monday"),
  (1, "Tuesday"),
  (2, "Wednesday"),
  (3, "Thursday"),
  (4, "Friday"),
  (5, "Saturday"),
  (6, "Sunday"),
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

        def get_weekday_to_display(self):
            return WEEKDAYS[self.weekday][1]

        def __unicode__(self):
            return self.venue.name + ' ' + self.get_weekday_to_display() + ' hours'

class VenueSpecialDays(BaseModel):
        venue = models.ForeignKey(Venue)
        holiday_date = models.DateField()
        closed = models.BooleanField(default=True)
        from_hour = models.TimeField(null=True, blank=True)
        to_hour = models.TimeField(null=True, blank=True)

        class Meta:
            unique_together = ('venue', 'holiday_date')

        def __unicode__(self):
            return self.venue + ' ' + self.holiday_date

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
        #if not self.bp_uri or len(self.bp_uri) == 0:
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
