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
        if not isinstance(value, basestring): return value
        value = pickle.loads(base64.b64decode(value))
        return value

    def get_db_prep_save(self, value):
        if value is None: return
        return base64.b64encode(pickle.dumps(value))
#==============================================

class Bar(BaseModel):
	email = models.EmailField(max_length=254)
	#secret = models.CharField()
	#salt = models.CharField()
	name = models.CharField()
	icon = models.URLField()
	lattitude = models.FloatField()
	longitude = models.FloatField()
	zipcode = models.PositiveIntegerField()

class AppUser(BaseModel):
	Gender_Options = (('Male', 'Male'), ('Female','Female'), ('Transgender','Transgender'))

	nickname = models.CharField()
	email = models.EmailField(max_length=254)
	secret = models.CharField()
	salt = models.CharField()
	age = models.PositiveIntegerField()
	sex = models.CharField(choices=Gender_Options)
	zipcode = models.PositiveIntegerField()
	favorite = models.CharField()

class DrinkType(BaseModel):
	bar = models.ForeignKey(Bar)
	type_name = models.CharField()
	
class Drink(BaseModel):
	bar = models.ForeignKey(Bar)
	drink_type = models.ForeignKey(DrinkType)
	name = models.CharField()
	price = models.DecimalField(decimal_places=2)
	
class Order(BaseModel):
	bar = models.ForeignKey(Bar)
	appuser = models.ForeignKey(AppUser)
	datetime = models.DateTimeField(auto_now_add=True)
	total = models.DecimalField(decimal_places=2)
	tax = models.DecimalField(decimal_places=2)
	sub_total = models.DecimalField(decimal_places=2)
	tip = models.DecimalField(decimal_places=2)
	grand_total = models.DecimalField(decimal_places=2)
	description = models.TextField(blank=True)
	drinks = SerializedDataField()


