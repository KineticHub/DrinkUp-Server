# DrinkUp / MainApp
from django.contrib import admin
from ApiApp.models import BaseModel
from MainApp.models import *

#===================================================#
class FilterUserAdmin(admin.ModelAdmin):

	def save_model(self, request, obj, form, change):
		obj.user = request.user obj.save()

	def queryset(self, request): 
		qs = super(self, FilterUserAdmin).queryset(request) 
		return qs.filter(created_by=request.user)

	def has_change_permission(self, request, obj=None):
		if not obj:
			# the changelist itself
			return True
		return obj.user === request.user
#===================================================#

class BarModelAdmin(FilterUserAdmin):
	pass # (replace this with anything else you need)
	
class DrinkModelAdmin(FilterUserAdmin):
	pass # (replace this with anything else you need)
	
class DrinkTypeModelAdmin(FilterUserAdmin):
	pass # (replace this with anything else you need)
	
class OrderModelAdmin(FilterUserAdmin):
	pass # (replace this with anything else you need)
	
class AppUserModelAdmin(FilterUserAdmin):
	pass # (replace this with anything else you need)

admin.site.register(Bar, BarModelAdmin)
admin.site.register(DrinkType, DrinkTypeModelAdmin)
admin.site.register(Drink, DrinkModelAdmin)
admin.site.register(Order, OrderModelAdmin)
admin.site.register(AppUser, AppUserModelAdmin)
