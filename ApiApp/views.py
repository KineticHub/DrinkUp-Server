#DrinkUp/ApiApp

#python helpers
import json
from datetime import datetime

#django view helpers
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect

#django models
from django.db.models.loading import get_model
from django.db.models import Q
from django.forms.models import model_to_dict
from django.db import models

#django authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#custom imports
from MainApp.models import *

#Facebook imports
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

def CreateAppUser(request):
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		
		try:
			find_user = User.objects.get(email=email)
			response = json.dumps({'status': 'duplicate',})
			return HttpResponse(response, mimetype="application/json", status=403)
			
		except User.DoesNotExist:
			new_user = User.objects.create_user(username = username, email = email, password = password)
			new_appuser = AppUser(user = new_user)
			
			new_user.save()
			new_appuser.save()
			
			user = authenticate(username=username, password=password)
			login(request, user)
			
			serialized_response = serializers.serialize('json', [ new_user, ])
			return HttpResponse(serialized_response, mimetype="application/json")

#NEED TO CHECK FOR DUPLICATE USERS
def LoginAppUser(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				# Redirect to a success page.
				#return redirect('/api/venues/all/')
				response = json.dumps({'status': 'success',})
				return HttpResponse(response, mimetype="application/json")
			else:
				response = json.dumps({'status': 'inactive',})
				return HttpResponse(response, mimetype="application/json", status=401)
				# Return a 'disabled account' error message
		else:
			response = json.dumps({'status': 'unauthorized',})
			return HttpResponse(response, mimetype="application/json", status=401)
			# Return an 'invalid login' error message.

def LogoutAppUser(request):
	logout(request)
	response = json.dumps({'status': 'success',})
	return HttpResponse(response, mimetype="application/json")

def EmptyTokenCall(request):
	request.META["CSRF_COOKIE_USED"] = True
	return HttpResponse('success')

def CheckAppUserAuthenticated(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			response = json.dumps({'status': 'success',})
			return HttpResponse(response, mimetype="application/json")
		else:
			response = json.dumps({'status': 'unauthorized',})
			return HttpResponse(response, mimetype="application/json", status=401)

@login_required
def PlaceOrderInQueue(request):
	if request.method == 'POST':
		pass


#BEGIN FB VIEWS
def index(request):
	return HttpResponse("""<button onclick="location.href='/facebook/login/'">Facebook Login</button>""")

#This view redirects the user to facebook in order to get the code that allows
#pyfb to obtain the access_token in the facebook_login_success view
def FacebookLogin(request):

	facebook = Pyfb(FACEBOOK_APP_ID)
	return HttpResponseRedirect(facebook.get_auth_code_url(redirect_uri=FACEBOOK_REDIRECT_URL))

#This view must be refered in your FACEBOOK_REDIRECT_URL. For example: http://www.mywebsite.com/facebook_login_success/
def FacebookLoginSuccess(request):

	code = request.GET.get('code')

	facebook = Pyfb(FACEBOOK_APP_ID)
	facebook.get_access_token(FACEBOOK_SECRET_KEY, code, redirect_uri=FACEBOOK_REDIRECT_URL)
	me = facebook.get_myself()
	
	if (type(me.name) == type(unicode())):
		return HttpResponse('It worked')

	welcome = "Welcome <b>%s</b>. Your Facebook login has been completed successfully!"
	return HttpResponse(welcome % me.username)

def FacebookMobileLogin(request):
	
	if request.method == 'POST':
	
		primary_user = 1
	
		facebook_id = request.POST.get('fb_user_id', None)
		facebook_email = request.POST.get('fb_user_email', None)
		token = request.POST.get('oauth_token', None)
		expiration = request.POST.get('expiration', None)
		creation = request.POST.get('created', None)
		
		#right now this only creates a new user, it does not authenticate an old one
		if not request.user.is_authenticated():
			if token and expiration and creation:
				new_token = OAuthToken(token = token, issued_at = datetime.fromtimestamp(float(creation)), expires_at = datetime.fromtimestamp(float(expiration)))
				new_token.save()
			
				facebook = Pyfb(FACEBOOK_APP_ID)
				facebook.set_access_token(token)
				me = facebook.get_myself()
			
				if (type(me.name) == type(unicode())):
				
					try:
						#also need to update to the current token
						find_fb_user = FacebookAppUser.objects.get(fb_uid=me.id)
						find_fb_user.oauth_token = new_token
						find_fb_user.save()
						user.backend = 'django.contrib.auth.backends.ModelBackend'
						login(request, user)
					
					except FacebookAppUser.DoesNotExist:
						birthday = datetime.strptime(me.birthday, '%m/%d/%Y')
						
						new_fb_user = FacebookAppUser(user_id = primary_user, fb_uid = me.id, fb_email = me.email, oauth_token = new_token)
						new_fb_user.save()
						
						new_user = User.objects.create_user(username = me.username, email = me.email, password = token)
						new_user.first_name = me.first_name
						new_user.last_name = me.last_name
						new_user.save()
						
						new_appuser = AppUser(user = new_user, facebook_user = new_fb_user, gender = me.gender, birthdate = birthday)
						new_appuser.save()
					
						return HttpResponse(me.__dict__)
		
		#same as above, only creates new one if a user logs into our server then to Facebook,
		#need to handle server login, then Facebook login and check if the user account is linked
		#should use fb_email for the check
		else:
			if token and expiration and creation:
				new_token = OAuthToken(token = token, issued_at = datetime.fromtimestamp(float(creation)), expires_at = datetime.fromtimestamp(float(expiration)))
				new_token.save()
				
				facebook = Pyfb(FACEBOOK_APP_ID)
				facebook.set_access_token(token)
				me = facebook.get_myself()
			
				if (type(me.name) == type(unicode())):
					try:
						#also need to update to the current token
						find_fb_user = FacebookAppUser.objects.get(fb_uid=me.id)
						if (find_fb_user.appuser.user == request.user):
							find_fb_user.oauth_token = new_token
							find_fb_user.save()
							response = json.dumps({'status': 'success',})
							return HttpResponse(response, mimetype="application/json")
						else:
							response = json.dumps({'status': 'unauthorized',})
							return HttpResponse(response, mimetype="application/json", status=401)
					
					except FacebookAppUser.DoesNotExist:
						birthday = datetime.strptime(me.birthday, '%m/%d/%Y')
						new_fb_user = FacebookAppUser(user_id = primary_user, fb_uid = me.id, fb_email = me.email, oauth_token = new_token)
						new_fb_user.save()
						
						current_user = request.user
						current_user.first_name = me.first_name
						current_user.last_name = me.last_name
						current_user.save()
						
						app_user = current_user.appuser
						app_user.gender = me.gender
						app_user.birthdate = birthday
						app_user.facebook_user = new_fb_user
						app_user.save()
						
						return HttpResponse('profile updated with facebook')

		return HttpResponse('failed')
