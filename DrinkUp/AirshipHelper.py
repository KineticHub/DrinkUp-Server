import urbanairship
from django.conf import settings

class AirshipHelper:
    
    def __init__(self):
        self.airship = urbanairship.Airship(settings.UA_APP_KEY, settings.UA_APP_MASTER_SECRET)

    def pushMessageForUser(self, message, user, status):
        self.airship.push({'aps': {'alert': message, 'badge':1, 'sound': 'default'}, 'status':status}, aliases=['appuser'+str(user.pk)])