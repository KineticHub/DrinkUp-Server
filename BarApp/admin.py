#DrinkUp/BarApp
from django.contrib import admin
from django.contrib.auth.models import User, Group
from VenueApp.models import *
from BarApp.models import *

# class VenueBarAdmin(FilterUserAdmin):
	# exclude = ('user',)
	
# class BarDrinkAdmin(FilterUserAdmin):
	# exclude = ('user',)

admin.site.register(VenueBar)#, VenueBarAdmin)
admin.site.register(BarDrink)#, BarDrinkAdmin)