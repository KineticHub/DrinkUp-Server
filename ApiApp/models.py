from django.db import models
from django.contrib.auth.models import User
import datetime

class BaseModel(models.Model):
	user = models.ForeignKey(User)
	created = models.DateField(editable=False)
	updated = models.DateTimeField(editable=False)
	
	def save(self):
		if not self.id:
			self.created = datetime.date.today()
		self.updated = datetime.datetime.today()
		super(BaseModel, self).save()

	class Meta:
		abstract = True
