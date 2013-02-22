#DrinkUp / MainApp
from django.db import models
from ApiApp.models import BaseModel

#==============================================
try:
	import cPickle as pickle
except:
	import pickle
import base64

class SerializedDataField(models.TextField):
	"""Because Django for some reason feels its needed to repeatedly call
	to_python even after it's been converted this does not support strings."""
	__metaclass__ = models.SubfieldBase

	def to_python(self, value):
		if value is None: return
		if value == '': return
		if not isinstance(value, basestring): return value
		value = pickle.loads(base64.b64decode(value))
		return value

	def get_db_prep_save(self, value):
		if value is None: return
		if value == '': return
		return base64.b64encode(pickle.dumps(value))
#==============================================

class Bar(BaseModel):
	email = models.EmailField(max_length=254)
	#secret = models.CharField()
	#salt = models.CharField()
	name = models.CharField(max_length=200)
	icon = models.URLField()
	lattitude = models.FloatField()
	longitude = models.FloatField()
	zipcode = models.PositiveIntegerField()

class AppUser(BaseModel):
	Gender_Options = (('Male', 'Male'), ('Female','Female'), ('Transgender','Transgender'))

	nickname = models.CharField(max_length=200)
	email = models.EmailField(max_length=254)
	secret = models.CharField(max_length=200)
	salt = models.CharField(max_length=200)
	age = models.PositiveIntegerField()
	sex = models.CharField(choices=Gender_Options, max_length=15)
	zipcode = models.PositiveIntegerField()
	favorite = models.CharField(max_length=200)

class DrinkType(BaseModel):
	bar = models.ForeignKey(Bar)
	type_name = models.CharField(max_length=200)
	
class Drink(BaseModel):
	bar = models.ForeignKey(Bar)
	drink_type = models.ForeignKey(DrinkType)
	name = models.CharField(max_length=200)
	price = models.DecimalField(decimal_places=2, max_digits=6)
	
class Order(BaseModel):
	bar = models.ForeignKey(Bar)
	appuser = models.ForeignKey(AppUser)
	datetime = models.DateTimeField(auto_now_add=True)
	total = models.DecimalField(decimal_places=2, max_digits=6)
	tax = models.DecimalField(decimal_places=2, max_digits=6)
	sub_total = models.DecimalField(decimal_places=2, max_digits=6)
	tip = models.DecimalField(decimal_places=2, max_digits=6)
	grand_total = models.DecimalField(decimal_places=2, max_digits=6)
	description = models.TextField(blank=True)
	drinks = SerializedDataField()


