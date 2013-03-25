# DrinkUp / MainApp
from django.contrib import admin
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from ApiApp.models import BaseModel
from MainApp.models import *

#===================================================#
class FilterUserAdmin(admin.ModelAdmin):

	def save_model(self, request, obj, form, change):
		try:
			obj.user
		except:
			obj.user = request.user
				
		obj.save()

	def queryset(self, request): 
		qs = super(FilterUserAdmin, self).queryset(request)
		if request.user.is_superuser:
						return qs
		return qs.filter(user=request.user)

	def has_change_permission(self, request, obj=None):
		if not obj:
			# the changelist itself
			return True
		if request.user.is_superuser:
						return True
		return obj.user == request.user

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "venue" and not request.user.is_superuser:
				kwargs["queryset"] = Venue.objects.filter(venue_owner=request.user)
				return db_field.formfield(**kwargs)
		if db_field.name == "bar" and not request.user.is_superuser:
				kwargs["queryset"] = VenueBar.objects.filter(user=request.user)
				return db_field.formfield(**kwargs)
		if db_field.name == "drink_type" and not request.user.is_superuser:
				kwargs["queryset"] = DrinkType.objects.filter(user=request.user)
				return db_field.formfield(**kwargs)
		return super(FilterUserAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
#===================================================#

class VenueModelAdmin(FilterUserAdmin):
	exclude = ('user', 'venue_owner',)
	
	def queryset(self, request):
		qs = super(FilterUserAdmin, self).queryset(request)
		if request.user.is_superuser:
						return qs
		return qs.filter(venue_owner=request.user)

	def has_change_permission(self, request, obj=None):
		if not obj:
			# the changelist itself
			return True
		if request.user.is_superuser:
						return True
		return obj.venue_owner == request.user

class VenueOwnerUserProfileModelAdmin(admin.ModelAdmin):
	pass
#	exclude = ('user',)

class VenueBarModelAdmin(FilterUserAdmin):
	exclude = ('user',)

class DrinkModelAdmin(FilterUserAdmin):
	exclude = ('user',)

class DrinkTypeModelAdmin(FilterUserAdmin):
	exclude = ('user',)

class DrinkOrderedForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(DrinkOrderedForm, self).__init__(*args, **kwargs)
		#self.fields['drink_name'] = forms.ModelChoiceField(queryset=Drink.objects.all())

	class Meta:
		model = DrinkOrdered

class DrinkOrderedInline(admin.StackedInline):
	model =  DrinkOrdered
	extra = 1
	form = DrinkOrderedForm

class OrderModelAdmin(FilterUserAdmin):
	exclude = ('user',)
	inlines = [
					DrinkOrderedInline,
					]
					
	def queryset(self, request): 
		qs = super(FilterUserAdmin, self).queryset(request)
		if request.user.is_superuser:
						return qs
		return qs.filter(bar__venue__venue_owner=request.user)
					
	def has_change_permission(self, request, obj=None):
		if not obj:
			# the changelist itself
			return True
		if request.user.is_superuser:
			return True
		return False
		
class AppUserModelAdmin(FilterUserAdmin):
	#exclude = ('user',)
	
	def queryset(self, request):
		queryset = AppUser.objects.all()
		return queryset
		
	def has_change_permission(self, request, obj=None):
		if not obj:
			# the changelist itself
			return True
		if request.user.is_superuser:
			return True
		return False

class FacebookAppUserModelAdmin(admin.ModelAdmin):
	exclude = ('user',)

class FourSquareAppUserModelAdmin(admin.ModelAdmin):
	exclude = ('user',)

admin.site.register(Venue, VenueModelAdmin)
admin.site.register(VenueOwnerUserProfile, VenueOwnerUserProfileModelAdmin)
admin.site.register(VenueBar, VenueBarModelAdmin)
admin.site.register(Drink, DrinkModelAdmin)
admin.site.register(DrinkType, DrinkTypeModelAdmin)
admin.site.register(Order, OrderModelAdmin)
#admin.site.register(DrinkOrdered)
admin.site.register(AppUser, AppUserModelAdmin)
admin.site.register(FacebookAppUser, FacebookAppUserModelAdmin)
admin.site.register(FourSquareAppUser, FourSquareAppUserModelAdmin)
