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

from MainApp.models import *

#imports for FB
from pyfb import Pyfb
from DrinkUp.settings import FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY, FACEBOOK_REDIRECT_URL

def AllBars(request):

    if request.method == 'GET':
        
        bars_to_return = Bar.objects.all()
        
        json_serializer = serializers.get_serializer("json")()
	response = json_serializer.serialize(bars_to_return, ensure_ascii=False)
	return HttpResponse(response, mimetype="application/json")

def AllDrinks(request):

    if request.method == 'GET':
        
        drinks_to_return = Drink.objects.filter()
        
        json_serializer = serializers.get_serializer("json")()
	response = json_serializer.serialize(drinks_to_return, ensure_ascii=False)
	return HttpResponse(response, mimetype="application/json")

def BarDrinks(request, bar_id):

    if request.method == 'GET':
        
        drinks_to_return = Drink.objects.filter(bar=bar_id)
        
        json_serializer = serializers.get_serializer("json")()
	response = json_serializer.serialize(drinks_to_return, ensure_ascii=False)
	return HttpResponse(response, mimetype="application/json")
        
		
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
		facebook_id = request.POST.get('fb_user_id', None)
		facebook_email = request.POST.get('fb_user_email', None)
		token = request.POST.get('oauth_token', None)
		expiration = request.POST.get('expiration')
		creation = request.POST.get('created')
		
		new_token = OAuthToken(token = token, issued_at = creation, expires_at = expiration)
		new_token.save()
		
		new_user = FacebookAppUser(fb_uid = facebook_id, fb_email = facebook_email, oauth_token = token)
		new_user.save()
		
		return HttpResponse("Yay!")