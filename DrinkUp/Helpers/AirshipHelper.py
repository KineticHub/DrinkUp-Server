import urbanairship as ua
from django.conf import settings


class AirshipHelper:
    def __init__(self):
        self.airship = ua.Airship(settings.UA_APP_KEY, settings.UA_APP_MASTER_SECRET)

    def push_message_for_user(self, message, user, status=None, order_id=None):
        #self.airship.push({'aps': {'alert': message, 'badge':1, 'sound': 'default'},
        # 'status':status}, aliases=[user.username])

        push = self.airship.create_push()
        push.audience = ua.or_(ua.alias(user.username))
        push.notification = ua.notification(ios=ua.ios(alert=message, sound='default', extra={'order_id': order_id}),
                                            android=ua.android(alert=message))
        push.device_types = ua.device_types('ios', 'android')
        push.send()
