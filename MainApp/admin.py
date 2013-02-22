# DrinkUp / MainApp
from django.contrib import admin
from ApiApp.models import BaseModel
from MainApp.models import *

#===================================================#
class FilterUserAdmin(admin.ModelAdmin):

	def save_model(self, request, obj, form, change):
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
#===================================================#

class BarModelAdmin(FilterUserAdmin):
	exclude = ('user',)
	
class DrinkModelAdmin(FilterUserAdmin):
	exclude = ('user',)
	
class DrinkTypeModelAdmin(FilterUserAdmin):
	exclude = ('user',)
	
class OrderModelAdmin(FilterUserAdmin):
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
