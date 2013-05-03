#DrinkUp/UsersApp
from django.contrib import admin
from UsersApp.models import *

admin.site.register(AppUser)
admin.site.register(FacebookAppUser)
admin.site.register(FourSquareAppUser)
admin.site.register(OAuthToken)
