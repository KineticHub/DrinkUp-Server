#DrinkUp.URLS
from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('DrinkUp',
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('ApiApp.views',
	url(r'^drinkup/venues/all/$', 'AllVenues'),
	url(r'^drinkup/venues/bars/(?P<venue_id>\d{1,10})/$', 'VenueBars'),
	url(r'^drinkup/venues/bars/drinks/types/(?P<bar_id>\d{1,10})/$', 'BarDrinkTypes'),
	url(r'^drinkup/venues/bars/drinks/(?P<bar_id>\d{1,10})/(?P<type_id>\d{1,10})/$', 'BarDrinksOfType'),
	
	url(r'^index/$', 'index'),
	url(r'^facebook_login/$', 'facebook_login'),
	url(r'^facebook_login_success/$', 'facebook_login_success'),
	url(r'^facebook_login/mobile/$', 'facebook_mobile_login'),
)
