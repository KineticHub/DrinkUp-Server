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
	url(r'^drinkup/bars/all/$', 'AllBars'),
	url(r'^drinkup/drinks/all/$', 'AllDrinks'),
	url(r'^drinkup/drinks/bar/(?P<bar_id>\d{1,10})/$', 'BarDrinks'),
	
	(r'^$', 'index'),
	(r'^facebook_login/$', 'facebook_login'),
	(r'^facebook_login_success/$', 'facebook_login_success'),
)
