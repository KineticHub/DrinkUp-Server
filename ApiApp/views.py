#DrinkUp/ApiApp

#python helpers
import json
from datetime import datetime
from decimal import *

#django view helpers
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
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
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

#model imports
from VenueApp.models import *
from BarApp.models import *
from UsersApp.models import *

#Facebook imports
from pyfb import Pyfb
from DrinkUp.settings import FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY, FACEBOOK_REDIRECT_URL

#django registration
from registration.views import *
from registration.backends import get_backend
#from registration.backends import default as registration_backend_default

#geopy imports
from geopy import geocoders
from geopy import distance
from geopy.point import Point

#BalancedPayments
from DrinkUp.BalancedHelper import BalancedPaymentsHelper

def CurrentLocation(request):
        if request.method == 'GET':
                g = geocoders.GoogleV3()
                if not lat or not long:
                        if zipcode:
                                place, (lat, long) = g.geocode(zipcode)
                        else:
                                response = json.dumps({'status': 'missing params',})
                                return HttpResponse(response, mimetype="application/json")

                url_request = url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng='+str(lat)+','+str(long)+'&sensor=false'
                place_returned = g.geocode_url(url, False)
                place_string = place_returned[0][-2]
                list_place = city = place_string.split(',')
                
                if len(list_place) > 3:
                        city = [list_place[-3], list_place[-2]]

                response = json.dumps({'status': 'duplicate',})
		return HttpResponse(response, mimetype="application/json", status=403)


def AllVenues(request):
	if request.method == 'GET':
		venues_to_return = Venue.objects.all()
		
		json_serializer = serializers.get_serializer("json")()
		response = json_serializer.serialize(venues_to_return, ensure_ascii=False)
		return HttpResponse(response, mimetype="application/json")

def VenuesNearLocation(request):
		if request.method == 'GET':
				zipcode = request.GET.get('zipcode')
				lat = request.GET.get('lat')
				long = request.GET.get('long')
				radius = request.GET.get('radius', '1.0')

				if not lat or not long:
						if zipcode:
                                                        g = geocoders.GoogleV3()
                                                        place, (lat, long) = g.geocode(zipcode)
						else:
                                                        response = json.dumps({'status': 'missing params',})
                                                        return HttpResponse(response, mimetype="application/json")
                        
				all_venues = Venue.objects.all()
				user_point = Point(str(lat)+";"+str(long)) #37.228272, -80.42313630000001 (Buruss)

				nearby_venues = []
				for venue in all_venues:
						venue_point = Point(str(venue.latitude)+";"+str(venue.longitude))
						if distance.distance(venue_point, user_point).miles < float(radius):
								nearby_venues.append(venue)

				json_serializer = serializers.get_serializer("json")()
                                response = json_serializer.serialize(nearby_venues, ensure_ascii=False)
                                return HttpResponse(response, mimetype="application/json")
                

def VenueBars(request, venue_id):
	if request.method == 'GET':
		bars_to_return = VenueBar.objects.filter(venue=venue_id)
		json_serializer = serializers.get_serializer("json")()
		response = json_serializer.serialize(bars_to_return, ensure_ascii=False)
		return HttpResponse(response, mimetype="application/json")

def BarDrinkTypes(request, bar_id):
	if request.method == 'GET':
		drinks = BarDrink.objects.filter(bar=bar_id)
		types_to_return = VenueDrinkType.objects.filter(bardrink__in=drinks).distinct()
		json_serializer = serializers.get_serializer("json")()
		response = json_serializer.serialize(types_to_return, ensure_ascii=False)
		return HttpResponse(response, mimetype="application/json")

def BarDrinksOfType(request, bar_id, type_id):
	if request.method == 'GET':
		drinks_to_return = BarDrink.objects.filter(bar=bar_id) if type_id == '0' else BarDrink.objects.filter(bar=bar_id, drink_type=type_id)
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
			#new_user = User.objects.create_user(username = username, email = email, password = password)
			#new_appuser = AppUser(user = new_user)
			
			#new_user.save()
			#new_appuser.save()

						backend = get_backend('registration.backends.default.DefaultBackend')
						if not backend.registration_allowed(request):
								return redirect(disallowed_url)

						kwargs = {}
						kwargs['username'] = request.POST['username']
						kwargs['email'] = request.POST['email']
						kwargs['password1'] = request.POST['password']

						new_user = backend.register(request, **kwargs)

						if new_user:
							new_appuser = AppUser(user = new_user)
							new_appuser.save()

						serialized_response = serializers.serialize('json', [ new_user, ])
						return HttpResponse(serialized_response, mimetype="application/json")

						#return errors about form, meant to be called as view
			#return register(request = request, backend = 'registration.backends.default.DefaultBackend')
			
			#user = authenticate(username=username, password=password)
			#login(request, user)
			
			#serialized_response = serializers.serialize('json', [ new_user, ])
			#return HttpResponse(serialized_response, mimetype="application/json")

#NEED TO CHECK FOR DUPLICATE USERS
def LoginAppUser(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		ctype = request.POST.get('credtype', None)

                if ctype is not None and ctype == 'staff':
                        if not user.is_staff:
                                return HttpResponseForbidden()
		
		if user is not None:
			if user.is_active:
				login(request, user)
				# Redirect to a success page.
				#return redirect('/api/venues/all/')
				#response = json.dumps({'status': 'success',})
				serialized_response = serializers.serialize('json', [user])
				return HttpResponse(serialized_response, mimetype="application/json")
				#return HttpResponse(response, mimetype="application/json")
			else:
				response = json.dumps({'status': 'inactive',})
				return HttpResponse(response, mimetype="application/json", status=401)
				# Return a 'disabled account' error message
		else:
			response = json.dumps({'status': 'unauthorized',})
			return HttpResponse(response, mimetype="application/json", status=401)
			# Return an 'invalid login' error message.

def LoginBarAdmin(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		
		if user is not None:
			if user.is_active and user.is_staff:
				login(request, user)
				bartender = BarAdminUser.objects.get(pk=request.user.id)
				# Redirect to a success page.
				#return redirect('/api/venues/all/')
				#response = json.dumps({'status': 'success',})
				serialized_response = serializers.serialize('json', [ user, bartender])
				return HttpResponse(serialized_response, mimetype="application/json")
				#return HttpResponse(response, mimetype="application/json")
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

def UpdateUserCard(request):
        if request.method == 'POST':
                if request.user.is_authenticated():
                        cc_uri = request.POST.get('uri', None)
                        if cc_uri is not None:
                                helper = BalancedPaymentsHelper()
                                helper.updateBuyerCreditCard(cc_uri=cc_uri, account_uri=request.user.appuser.bp_account)
                                response = json.dumps({'status': 'success',})
                                return HttpResponse(response, mimetype="application/json")
                        else:
                                response = json.dumps({'status': 'invalid',})
                                return HttpResponse(response, mimetype="application/json", status=401)
                        
                        
                        

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

##################
#BEGIN ORDER VIEWS

#NEED TO VERIFY THAT USER IS A BARTENDER
def CreateNewOrder(request):
		if not request.user.is_authenticated():
                        return HttpResponseForbidden()
				
		if request.method == 'POST': #and request.user.is_authenticated():
			bar_id = request.POST.get('bar_id', None)
			appuser = request.user.appuser
			total = request.POST.get('total', None)
			tax = request.POST.get('tax', None)
			sub_total = request.POST.get('sub_total', None)
			tip = request.POST.get('tip', None)
			fees = request.POST.get('fees', None)
			grand_total = request.POST.get('grand_total', None)
			description = request.POST.get('description', '')
			drinks = request.POST.get('drinks', None)

			if bar_id and total and tax and sub_total and tip and fees and grand_total and drinks:
				primary_user = 1
				bar = VenueBar.objects.get(pk=bar_id)
				drinks_data = json.loads(drinks)
				
				new_order = BarOrder(user_id=primary_user, bar=bar, appuser=appuser, total=total, tax=tax, sub_total=sub_total, tip=tip, fees=fees, grand_total=grand_total, current_status=1, description=description)
				new_order.save()
				
				for drink in drinks_data:
					drink_type = VenueDrinkType.objects.get(pk=int(drink['drink_type']))
					price = Decimal(drink['price'])
					is_happyhour = False
					if bar.happyhour_start < datetime.now().time() and bar.happyhour_end > datetime.now().time():
						price = Decimal(drink['happyhour_price'])
						is_happyhour = True
					new_drink_ordered = BarDrinkOrdered(order=new_order, drink_name=drink['name'], quantity=int(drink['quantity']), unit_price=price, drink_type=drink_type.name, ordered_during_happyhour=is_happyhour)
					new_drink_ordered.save()

				serialized_response = serializers.serialize('json', [ new_order, ])
				return HttpResponse(serialized_response, mimetype="application/json")

@staff_member_required
def GetNewOrdersForBarSince(request, bar_id=0, since_time=0, status=0):
	
	if request.method == 'GET':

                bartender = BarAdminUser.objects.get(pk=request.user.id)

                if bar_id == 0:
                        bar_id = bartender.bar.pk
                
		#CHECK THE LAST FILTER DATETIME COMPARISON
		drinkOrders = BarDrinkOrdered.objects.select_related("order").filter(order__bar=bar_id).filter(order__created__gte = datetime.fromtimestamp(float(since_time))).filter(order__current_status=status)
			
		all_orders = []
		from itertools import groupby
		for k, g in groupby(drinkOrders, lambda x: x.order):
			user = json.loads(serializers.serialize('json', [k.appuser, ], relations = { 'user': { 'fields': ( 'username', 'first_name', 'last_name', 'email', ) },  'facebook_user': { 'fields': ( 'fb_uid', 'fb_email', ) }, } ) )[0]
			order = json.loads(serializers.serialize('json', [ k, ]))[0]
			drinkOrders = []
			for item in list(g):
				drinkOrders.append(json.loads(serializers.serialize('json', [item, ]))[0])
			tempOrderDict = {'appuser':user, 'order':order, 'drinks':drinkOrders}
			all_orders.append(tempOrderDict)
		
		response = json.dumps(all_orders)
		return HttpResponse(response, mimetype="application/json")
						
@staff_member_required
def GetOrdersForBarWithStatus(request, bar_id=0, status=0):
		if request.method == 'GET':
			#orders = Order.objects.filter(bar=bar_id).filter(current_status=status)

                        bartender = BarAdminUser.objects.get(pk=request.user.id)

                        if bar_id == 0:
                                bar_id = bartender.bar.pk
			
			drinkOrders = BarDrinkOrdered.objects.select_related("order").filter(order__bar=bar_id).filter(order__current_status=status)
			
			all_orders = []
			from itertools import groupby
			for k, g in groupby(drinkOrders, lambda x: x.order):
				user = json.loads(serializers.serialize('json', [k.appuser, ], relations = { 'user': { 'fields': ( 'username', 'first_name', 'last_name', 'email', ) },  'facebook_user': { 'fields': ( 'fb_uid', 'fb_email', ) }, } ) )[0] 
				order = json.loads(serializers.serialize('json', [ k, ]))[0]
				drinkOrders = []
				for item in list(g):
					drinkOrders.append(json.loads(serializers.serialize('json', [item, ]))[0])
				tempOrderDict = {'appuser':user, 'order':order, 'drinks':drinkOrders}
				all_orders.append(tempOrderDict)
			
			response = json.dumps(all_orders)
			return HttpResponse(response, mimetype="application/json")

@staff_member_required
def GetOrdersForBarWithStatusInTimeRange(request, bar_id=0, status=0, time_start = 0, time_end = datetime.today()):
		if request.method == 'GET':

                        bartender = BarAdminUser.objects.get(pk=request.user.id)

                        if bar_id == 0:
                                bar_id = bartender.bar.pk
                        
			#orders = Order.objects.filter(bar=bar_id).filter(current_status=status).filter(update__range=[time_start, time_end])
			time_start = datetime.fromtimestamp(float(time_start))
			time_end = datetime.fromtimestamp(float(time_end))
			drinkOrders = BarDrinkOrdered.objects.select_related("order").filter(order__bar=bar_id).filter(order__current_status=status).filter(order__updated__range=[datetime.fromtimestamp(float(time_start)), datetime.fromtimestamp(float(time_end))])
			
			all_orders = []
			from itertools import groupby
			for k, g in groupby(drinkOrders, lambda x: x.order):
				order = json.loads(serializers.serialize('json', [ k, ]))[0]
				drinkOrders = []
				for item in list(g):
					drinkOrders.append(json.loads(serializers.serialize('json', [item, ]))[0])
				tempOrderDict = {'order':order, 'drinks':drinkOrders}
				all_orders.append(tempOrderDict)
			
			response = json.dumps(all_orders)
			return HttpResponse(response, mimetype="application/json")

@staff_member_required
def UpdateOrderStatus(request):
		#if not request.user.is_authenticated():
                        #return HttpResponseForbidden()
				
	if request.method == 'POST':
                order_id = request.POST.get('order_id', None)
                new_status = request.POST.get('new_status', None)

                if order_id and new_status:
                        order = BarOrder.objects.get(pk=order_id)
                        order.current_status = new_status
                        order.save()
                        #response = json.dumps({'status': 'success',})
                        serialized_response = serializers.serialize('json', [ order, ])
                        return HttpResponse(serialized_response, mimetype="application/json")

#END ORDER VIEWS
##################
##################
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
		
		if not request.user.is_authenticated():
			if token and expiration and creation:
				new_token = OAuthToken(token = token, issued_at = datetime.fromtimestamp(float(creation)), expires_at = datetime.fromtimestamp(float(expiration)))
				new_token.save()
			
				facebook = Pyfb(FACEBOOK_APP_ID)
				facebook.set_access_token(token)
				me = facebook.get_myself()
			
				if (type(me.name) == type(unicode())):
				
					try:
						find_fb_user = FacebookAppUser.objects.get(fb_uid=me.id)
						find_fb_user.oauth_token = new_token
						find_fb_user.save()
						user = find_fb_user.appuser.user
						user.backend = 'django.contrib.auth.backends.ModelBackend'
						login(request, user)
						#response = json.dumps({'status': 'success', 'user':user})
						serialized_response = serializers.serialize('json', [find_fb_user.appuser, ], relations = { 'user': { 'fields': ( 'username', 'first_name', 'last_name', 'email', ) },  'facebook_user': { 'fields': ( 'fb_uid', 'fb_email', ) }, } )
						return HttpResponse(serialized_response, mimetype="application/json")
					
					except FacebookAppUser.DoesNotExist:

						birthday = None
						if hasattr(me, 'birthday'):
							birthday = datetime.strptime(me.birthday, '%m/%d/%Y')
						
						new_fb_user = FacebookAppUser(user_id = primary_user, fb_uid = me.id, fb_email = me.email, oauth_token = new_token)
						new_fb_user.save()
						
						new_user = User.objects.create_user(username = me.username, email = me.email, password = token)
						new_user.first_name = me.first_name
						new_user.last_name = me.last_name
						new_user.save()
						
						new_appuser = AppUser(user = new_user, facebook_user = new_fb_user, gender = me.gender, birthdate = birthday)
						new_appuser.save()

						new_user.backend = 'django.contrib.auth.backends.ModelBackend'
						login(request, new_user)

                                                #response = json.dumps({'status': 'success', 'user':new_user})
                                                #serialized_response = serializers.serialize('json', [ new_user, ])
						#return HttpResponse(me.__dict__)
						serialized_response = serializers.serialize('json', [new_appuser, ], relations = { 'user': { 'fields': ('username', 'first_name', 'last_name', 'email', ) },  'facebook_user': { 'fields': ( 'fb_uid', 'fb_email', ) }, } ) 
                                                return HttpResponse(serialized_response, mimetype="application/json")
		
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
						fb_user = FacebookAppUser.objects.get(fb_uid=me.id)
						user = fb_user.appuser.user
						#response = json.dumps({'status': 'success', 'user':user, 'fb_user':fb_user})
						#serialized_response = serializers.serialize('json', [ user, fb_user, ])
						#return HttpResponse(me.__dict__)
						serialized_response = serializers.serialize('json', [fb_user.appuser, ], relations = { 'user': { 'fields': ( 'username', 'first_name', 'last_name', 'email', ) },  'facebook_user': { 'fields': ( 'fb_uid', 'fb_email', ) }, } )
                                                return HttpResponse(serialized_response, mimetype="application/json")
						#return HttpResponse(response, mimetype="application/json")
						#if (find_fb_user.appuser.user == request.user):
							#find_fb_user.oauth_token = new_token
							#find_fb_user.save()
							#response = json.dumps({'status': 'success',})
							#return HttpResponse(response, mimetype="application/json")
						#else:
							#response = json.dumps({'status': 'unauthorized',})
							#return HttpResponse(response, mimetype="application/json", status=401)
					
					except FacebookAppUser.DoesNotExist:
						birthday = None
						if hasattr(me, 'birthday'):
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

		return HttpResponse('failed', status=400)
#END FB VIEWS
##################
