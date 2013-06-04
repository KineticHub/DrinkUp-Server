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
	url(r'^accounts/', include('registration.urls')),
)

urlpatterns += patterns('ApiApp.views',

	url(r'^api/token/$', 'EmptyTokenCall'),

	url(r'^api/venues/all/$', 'AllVenues'),
        url(r'^api/venues/nearby/$', 'VenuesNearLocation'),
	url(r'^api/venues/bars/(?P<venue_id>\d{1,10})/$', 'VenueBars'),
	url(r'^api/venues/bars/drinks/types/(?P<bar_id>\d{1,10})/$', 'BarDrinkTypes'),
	url(r'^api/venues/bars/drinks/(?P<bar_id>\d{1,10})/(?P<type_id>\d{1,10})/$', 'BarDrinksOfType'),

        url(r'^api/user/location/$', 'CurrentLocation'),
	url(r'^api/user/login/$', 'LoginAppUser'),
	url(r'^api/user/create/$', 'CreateAppUser'),
	url(r'^api/user/logout/$', 'LogoutAppUser'),
	url(r'^api/user/authenticated/$', 'CheckAppUserAuthenticated'),
        url(r'^api/user/update_card/$', 'UpdateUserCard'),
        url(r'^api/user/valid_card/$', 'CurrentUserCard'),
        url(r'^api/user/invalidate_card/$', 'InvalidateUserCard'),
        url(r'^api/user/picture_saved/$', 'UserProfilePictureSaved'),
        url(r'^api/user/picture_removed/$', 'UserProfilePictureRemoved'),
        url(r'^api/user/order_history/$', 'GetUserOrderHistory'),
                        
        url(r'^api/bartender/login/$', 'LoginBarAdmin'),

    url(r'^api/orders/create/$', 'CreateNewOrder'),
    url(r'^api/orders/update/$', 'UpdateOrderStatus'),
    url(r'^api/orders/(?P<bar_id>\d{1,10})/(?P<status>\d{1,2})/$', 'GetOrdersForBarWithStatus'),
    url(r'^api/orders/since/(?P<bar_id>\d{1,10})/(?P<since_time>\d{1,10})/(?P<status>\d{1,10})/$', 'GetNewOrdersForBarSince'),
    url(r'^api/orders/(?P<bar_id>\d{1,10})/(?P<status>\d{1,2})/(?P<time_start>\d{1,10})/(?P<time_end>\d{1,10})/$', 'GetOrdersForBarWithStatusInTimeRange'),

	url(r'^index/$', 'index'),
	url(r'^facebook/login/$', 'FacebookLogin'),
	url(r'^facebook/login/success/$', 'FacebookLoginSuccess'),
	url(r'^facebook/mobile_login/$', 'FacebookMobileLogin'),
)

urlpatterns += patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/admin/'}),
    (r'^grappelli/', include('grappelli.urls')),
)
