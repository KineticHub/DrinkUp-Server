# DrinkUp / MainApp
from django.contrib import admin
from ApiApp.models import BaseModel
from MainApp.models import *

#===================================================#
class FilterUserAdmin(admin.ModelAdmin):

	def save_model(self, request, obj, form, change):
                if not request.user.is_superuser:
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

class DrinkOrderedInline(admin.StackedInline):
        exclude = ('user',)
        model =  DrinkOrdered
        extra = 1

class OrderModelAdmin(FilterUserAdmin):
	exclude = ('user',)
        inlines = [
                DrinkOrderedInline,
                    ]
        extras = 0
	
class AppUserModelAdmin(FilterUserAdmin):
	exclude = ('user',)
	
	def queryset(self, request):
                queryset = AppUser.objects.all()
                return queryset

admin.site.register(Bar, BarModelAdmin)
admin.site.register(DrinkType, DrinkTypeModelAdmin)
admin.site.register(Drink, DrinkModelAdmin)
admin.site.register(Order, OrderModelAdmin)
admin.site.register(AppUser, AppUserModelAdmin)
