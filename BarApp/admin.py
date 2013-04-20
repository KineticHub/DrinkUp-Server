#DrinkUp/BarApp
from django.contrib import admin
from django.contrib.auth.models import User, Group
from VenueApp.models import *
from BarApp.models import *

class VenueBarAdmin(admin.ModelAdmin):
	exclude = ('user',)
	
	def queryset(self, request): 
		qs = super(VenueBarAdmin, self).queryset(request)
		if request.user.is_superuser:
				return qs
		try:
			venue_admin = VenueAdminUser.objects.get(pk=request.user.id)
			return qs.filter(venue=venue_admin.venue)
		except:
			try:
				bar_admin = BarAdminUser.objects.get(pk=request.user.id)
				return qs.filter(venue=bar_admin.venue)
			except:
				# THIS SHOULD NOT HAPPEN, BUT SMOOTH HANDING IS GOOD
				pass
		return None
	
class BarDrinkAdmin(admin.ModelAdmin):
	exclude = ('user',)
	
	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='Bar Admins').exists():
			return self.readonly_fields + ('bar',)
		return self.readonly_fields
	
	def queryset(self, request): 
		qs = super(BarDrinkAdmin, self).queryset(request)
		if request.user.is_superuser:
				return qs
		try:
			venue_admin = VenueAdminUser.objects.get(pk=request.user.id)
			return qs.filter(bar__venue=venue_admin.venue)
		except:
			try:
				bar_admin = BarAdminUser.objects.get(pk=request.user.id)
				return qs.filter(bar=bar_admin.bar)
			except:
				# THIS SHOULD NOT HAPPEN, BUT SMOOTH HANDING IS GOOD
				pass
		return None
		
class BarOrderAdmin(admin.ModelAdmin):
	exclude = ('user',)
	
	def get_readonly_fields(self, request, obj=None):
		if not request.user.is_superuser:
			return self.readonly_fields + ('bar', 'appuser', 'total', 'tax', 'sub_total', 'tip', 'fees', 'grand_total', 'current_status', 'description', 'payment_processed', 'transaction_id', )
		return self.readonly_fields
	
	def queryset(self, request): 
		qs = super(BarOrderAdmin, self).queryset(request)
		if request.user.is_superuser:
				return qs
		try:
			venue_admin = VenueAdminUser.objects.get(pk=request.user.id)
			return qs.filter(bar__venue=venue_admin.venue)
		except:
			try:
				bar_admin = BarAdminUser.objects.get(pk=request.user.id)
				return qs.filter(bar__venue=bar_admin.venue)
			except:
				# THIS SHOULD NOT HAPPEN, BUT SMOOTH HANDING IS GOOD
				pass
		return None

admin.site.register(VenueBar, VenueBarAdmin)
admin.site.register(BarDrink, BarDrinkAdmin)
admin.site.register(BarOrder)