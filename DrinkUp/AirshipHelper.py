import airship
from django.conf import settings

class AirshipHelper:
    
    def __init__(self):
        self.airship = urbanairship.Airship(settings.UA_APP_KEY, settings.UA_APP_MASTER_SECRET)

    def pushMessageForUser(message, user)
        airship.push({'aps': {'alert': message, 'badge':'1'}}, alias=['appuser'+user.pk])
