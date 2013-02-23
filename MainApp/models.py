#DrinkUp / MainApp
from django.db import models
from ApiApp.models import BaseModel

class Bar(BaseModel):
	email = models.EmailField(max_length=254)
	name = models.CharField(max_length=200)
	icon = models.URLField()
	lattitude = models.FloatField()
	longitude = models.FloatField()
	zipcode = models.PositiveIntegerField()

	def __unicode__(self):
		return self.name
		
	class Meta:
		ordering = ['name']

class AppUser(BaseModel):
	
	Gender_Options = (('Male', 'Male'), ('Female','Female'), ('Transgender','Transgender'))

	nickname = models.CharField(max_length=200)
	email = models.EmailField(max_length=254)
	#secret = models.CharField(max_length=200)
	#salt = models.CharField(max_length=200)
	age = models.PositiveIntegerField()
	sex = models.CharField(choices=Gender_Options, max_length=15)
	zipcode = models.PositiveIntegerField()
	favorite = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nickname
		
	class Meta:
		ordering = ['nickname']

class DrinkType(BaseModel):
	bar = models.ForeignKey(Bar)
	type_name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.type_name
		
	class Meta:
		ordering = ['type_name']
	
class Drink(BaseModel):
	bar = models.ForeignKey(Bar)
	drink_type = models.ForeignKey(DrinkType)
	name = models.CharField(max_length=200)
	price = models.DecimalField(decimal_places=2, max_digits=6)

	def __unicode__(self):
		return self.name
		
	class Meta:
		ordering = ['name']
	
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

	def __unicode__(self):
		return str(self.appuser)
		
	class Meta:
		ordering = ['datetime']

class DrinkOrdered(BaseModel):
	order = models.ForeignKey(Order)
	drink = models.ForeignKey(Drink)
	quantity = models.PositiveIntegerField()

