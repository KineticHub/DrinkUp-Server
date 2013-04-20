#DrinkUp/VenueApp
from django.contrib import admin
from VenueApp.models import *
from BarApp.models import *

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group

###################################################################	

class VenueAdminUserChangeForm(UserChangeForm):
	class Meta:
		model = VenueAdminUser

class VenueAdminUserAdmin(UserAdmin):
		
	form = VenueAdminUserChangeForm

	add_fieldsets = ((None, { 'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2')}),)
	add_form = UserCreationForm
	
	fieldsets = ((None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'venue')}),)
	restricted_fieldsets = ((None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'is_active')}),)

	def get_readonly_fields(self, request, obj=None):
		if not request.user.is_superuser:
			return self.readonly_fields + ('venue',)
		return self.readonly_fields
	
	def queryset(self, request):
		if request.user.is_superuser:
			return VenueAdminUser.objects.all()
		venue_admin = VenueAdminUser.objects.get(pk=request.user.id)
		return VenueAdminUser.objects.filter(venue = venue_admin.venue)

	def get_fieldsets(self, request, obj=None):
		if obj:
			return self.fieldsets
		else:
			return self.add_fieldsets

	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:
			try:
				venue_admin = VenueAdminUser.objects.get(pk=request.user.id)
				obj.venue = venue_admin.venue
			except:
				obj.is_active = False
		obj.is_staff = True
		obj.save()

		try:
			group = Group.objects.get(name='Venue Admins')
		except Group.DoesNotExist:
			# group should exist, but this is just for safety's sake, it case the improbable should happen
			pass
		else:
			obj.groups.add(group)

###################################################################			

class BarAdminUserChangeForm(UserChangeForm):
	class Meta:
		model = BarAdminUser

class BarAdminUserAdmin(UserAdmin):
	form = BarAdminUserChangeForm

	add_fieldsets = ((None, { 'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2', 'bar')}),)
	add_form = UserCreationForm
	
	fieldsets = ((None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'venue', 'bar')}),)
	restricted_fieldsets = ((None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'is_active')}),)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "bar" and not request.user.is_superuser:
			venue_admin = VenueAdminUser.objects.get(pk=request.user.id)
			kwargs["queryset"] = VenueBar.objects.filter(venue=venue_admin.venue)
			return db_field.formfield(**kwargs)
		return super(BarAdminUserAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
		
	def get_readonly_fields(self, request, obj=None):
		if not request.user.is_superuser:
			return self.readonly_fields + ('venue',)
		return self.readonly_fields
	
	def queryset(self, request):
		if request.user.is_superuser:
			return BarAdminUser.objects.all()
		venue_admin = VenueAdminUser.objects.get(pk=request.user.id)
		return BarAdminUser.objects.filter(venue = venue_admin.venue)

	def get_fieldsets(self, request, obj=None):
		if obj:
			return self.fieldsets
		else:
			return self.add_fieldsets
	
	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:
			try:
				venue_admin = VenueAdminUser.objects.get(pk=request.user.id)
				obj.venue = venue_admin.venue
			except:
				obj.is_active = False
		obj.is_staff = True
		obj.save()
		try:
			group = Group.objects.get(name='Bar Admins')
		except Group.DoesNotExist:
			# group should exist, but this is just for safety's sake, it case the improbable should happen
			pass
		else:
			obj.groups.add(group)
			
###################################################################	

class VenueDrinkTypeAdmin(admin.ModelAdmin):
	exclude = ('user',)
			
	def get_readonly_fields(self, request, obj=None):
		if not  request.user.is_superuser:
			return self.readonly_fields + ('venue',)
		return self.readonly_fields
	
	def save_model(self, request, obj, form, change):
		try:
			obj.user
		except:
			obj.user = request.user
			
		if not request.user.is_superuser:
                    try:
                        venue_admin = VenueAdminUser.objects.get(pk=request.user.id)
                        obj.venue = venue_admin.venue
                    except:
                        try:
                            bar_admin = BarAdminUser.objects.get(pk=request.user.id)
                            obj.venue = bar_admin.venue
                        except:
                            # THIS SHOULD NOT HAPPEN, BUT SMOOTH HANDLING IS GOOD
                            pass
		
		obj.save()
	
	def queryset(self, request): 
		qs = super(VenueDrinkTypeAdmin, self).queryset(request)
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
			
admin.site.register(Venue)
admin.site.register(VenueAdminUser, VenueAdminUserAdmin)
admin.site.register(BarAdminUser, BarAdminUserAdmin)
admin.site.register(VenueDrinkType, VenueDrinkTypeAdmin)