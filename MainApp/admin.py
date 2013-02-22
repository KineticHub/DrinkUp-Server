# DrinkUp / MainApp
from django.contrib import admin
from ApiApp.models import BaseModel
from MainApp.models import *

#===================================================#
class FilterUserAdmin(admin.ModelAdmin):

	def save_model(self, request, obj, form, change):
		if not obj.user:
			obj.user = request.user
		obj.save()

	def queryset(self, request): 
		qs = super(FilterUserAdmin, self).queryset(request) 
		return qs.filter(user=request.user)

	def has_change_permission(self, request, obj=None):
		if not obj:
			# the changelist itself
			return True
		return obj.user == request.user
		
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "bar":
			kwargs["queryset"] = Bar.objects.filter(user=request.user)
			return db_field.formfield(**kwargs)
		if db_field.name == "drink_type":
			kwargs["queryset"] = DrinkType.objects.filter(user=request.user)
			return db_field.formfield(**kwargs)
		return super(FilterUserAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
#===================================================#

class BarModelAdmin(FilterUserAdmin):
	exclude = ('user',)
	
class DrinkModelAdmin(FilterUserAdmin):
	exclude = ('user',)
	
class DrinkTypeModelAdmin(FilterUserAdmin):
	exclude = ('user',)
	
class OrderModelAdmin(FilterUserAdmin):

	def queryset(self, request): 
		qs = super(FilterUserAdmin, self).queryset(request)
		bars = Bar.objects.filter(user=request.user)
		return qs.filter(bar__pk__in = [bar.pk for bar in bars])

	exclude = ('user',)
	
class AppUserModelAdmin(FilterUserAdmin):
	exclude = ('user',)

admin.site.register(Bar, BarModelAdmin)
admin.site.register(DrinkType, DrinkTypeModelAdmin)
admin.site.register(Drink, DrinkModelAdmin)
admin.site.register(Order, OrderModelAdmin)
admin.site.register(AppUser, AppUserModelAdmin)

##admin.site.register(Bar)
##admin.site.register(DrinkType)
##admin.site.register(Drink)
##admin.site.register(Order)
##admin.site.register(AppUser)
