#DrinkUp/ApiApp

import json
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from django.db.models import Q
from django.forms.models import model_to_dict
import datetime

from django.db import models
from django.contrib.auth.models import User

from MainApp.models import *

#imports for FB
from pyfb import Pyfb
from DrinkUp.settings import FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY, FACEBOOK_REDIRECT_URL

def AllVenues(request):
	if request.method == 'GET':
		venues_to_return = Venue.objects.all()
		
		json_serializer = serializers.get_serializer("json")()
		response = json_serializer.serialize(venues_to_return, ensure_ascii=False)
		return HttpResponse(response, mimetype="application/json")

def VenueBars(request, venue_id):
	if request.method == 'GET':
		bars_to_return = VenueBar.objects.filter(venue=venue_id)
		json_serializer = serializers.get_serializer("json")()
		response = json_serializer.serialize(bars_to_return, ensure_ascii=False)
		return HttpResponse(response, mimetype="application/json")

def BarDrinkTypes(request, bar_id):
	if request.method == 'GET':
		drinks = Drink.objects.filter(bar=bar_id)
		types_to_return = DrinkType.objects.filter(drink__in=drinks)
		json_serializer = serializers.get_serializer("json")()
		response = json_serializer.serialize(types_to_return, ensure_ascii=False)
		return HttpResponse(response, mimetype="application/json")

def BarDrinksOfType(request, bar_id, type_id):
	if request.method == 'GET':
		drinks_to_return = Drink.objects.filter(bar=bar_id) if type_id == '0' else Drink.objects.filter(bar=bar_id, drink_type=type_id)
		json_serializer = serializers.get_serializer("json")()
		response = json_serializer.serialize(drinks_to_return, ensure_ascii=False)
		return HttpResponse(response, mimetype="application/json")

def AppUserLogin(request):
	if request.method == 'POST':
		pass


#BEGIN FB VIEWS
def index(request):
	return HttpResponse("""<button onclick="location.href='/Project/facebook_login'">Facebook Login</button>""")

#This view redirects the user to facebook in order to get the code that allows
#pyfb to obtain the access_token in the facebook_login_success view
def facebook_login(request):

	facebook = Pyfb(FACEBOOK_APP_ID)
	return HttpResponseRedirect(facebook.get_auth_code_url(redirect_uri=FACEBOOK_REDIRECT_URL))

#This view must be refered in your FACEBOOK_REDIRECT_URL. For example: http://www.mywebsite.com/facebook_login_success/
def facebook_login_success(request):

	code = request.GET.get('code')

	facebook = Pyfb(FACEBOOK_APP_ID)
	facebook.get_access_token(FACEBOOK_SECRET_KEY, code, redirect_uri=FACEBOOK_REDIRECT_URL)
	me = facebook.get_myself()

	welcome = "Welcome <b>%s</b>. Your Facebook login has been completed successfully!"
	return HttpResponse(welcome % me.__dict__)

@csrf_exempt
def facebook_mobile_login(request):
	
	if request.method == 'POST':
	
		primary_user = 1#User.objects.get(pk=1)
	
		facebook_id = request.POST.get('fb_user_id', None)
		facebook_email = request.POST.get('fb_user_email', None)
		token = request.POST.get('oauth_token', None)
		expiration = request.POST.get('expiration', None)
		creation = request.POST.get('created', None)
		
		if token and expiration and creation:
			new_token = OAuthToken(token = token, issued_at = datetime.datetime.fromtimestamp(float(creation)), expires_at = datetime.datetime.fromtimestamp(float(expiration)))
			new_token.save()
			facebook = Pyfb(FACEBOOK_APP_ID)
			facebook.set_access_token(token)
			me = facebook.get_myself()
			return HttpResponse(me.__dict__)
		
			#new_user = FacebookAppUser(user_id = primary_user, fb_uid = facebook_id, fb_email = facebook_email, oauth_token = new_token)
			#new_user.save()
		
			return HttpResponse("Yay!")
		return HttpResponse(facebook_id)
