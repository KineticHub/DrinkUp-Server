from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import utc

class BaseModel(models.Model):
	user = models.ForeignKey(User)
	created = models.DateTimeField(editable=False)
	updated = models.DateTimeField(editable=False)
	
	def save(self):
		if not self.id:
			self.created = datetime.datetime.utcnow().replace(tzinfo=utc)
		self.updated = datetime.datetime.utcnow().replace(tzinfo=utc)
		super(BaseModel, self).save()

	class Meta:
		abstract = True
