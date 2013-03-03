from django.db import models
from django.contrib.auth.models import User
import datetime

class BaseModel(models.Model):
	user = models.ForeignKey(User)
	created = models.DateTimeField(editable=False)
	updated = models.DateTimeField(editable=False)
	
	def save(self):
		if not self.id:
			self.created = datetime.datetime.now()
		self.updated = datetime.datetime.now()
		super(BaseModel, self).save()

	class Meta:
		abstract = True
