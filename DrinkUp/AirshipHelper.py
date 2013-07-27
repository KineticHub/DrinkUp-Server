import urbanairship as ua
from django.conf import settings


class AirshipHelper:
	def __init__(self):
		self.airship = ua.Airship(settings.UA_APP_KEY_PROD, settings.UA_APP_MASTER_SECRET_PROD)

	def pushMessageForUser(self, message, user, status):
		#self.airship.push({'aps': {'alert': message, 'badge':1, 'sound': 'default'}, 'status':status}, aliases=[user.username])

		push = self.airship.create_push()
		push.audience = ua.or_(ua.alias(user.username))
		push.notification = ua.notification(alert=message, badge='+1')
		push.device_types = ua.device_types('ios', 'android')
		push.send()
