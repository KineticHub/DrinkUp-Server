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
)
