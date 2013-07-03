__author__ = 'Kinetic'

from email_manager.feature_send_email import EmailSender
from email_manager.models import EmailType, UserEmailPreferences

def send_email(email_args):
    users = email_args['users']
    subject = email_args['subject']
    content = email_args['content']
    html_content = email_args['html_content']
    email_type = email_args['email_type']
    additional_emails=None
    EmailSender().send_email_to_users(users, additional_emails, subject, content, html_content, email_type)

def send_order_receipt_email(order):
    email_args={}
    email_args['users'] = [order.appuser.user,]
    email_args['subject'] = 'Your receipt for DrinkUp order {order_id}'.format(order_id=order.pk)
    email_args['content'] = 'This is where the order information will be given.'
    email_args['html_content'] = 'This is where the <b>HTMML</b> version of the order information will be given.'
    email_args['email_type'] = EmailType.objects.get(pk=1)
    send_email(email_args)



# from django.core.mail import send_mail, BadHeaderError
#
# def send_email(email_args):
#     subject = email_args['subject']
#     message = email_args['message']
#     from_email = email_args['from_email']
#     if subject and message and from_email:
#         try:
#             send_mail(subject, message, from_email, ['k.alnajar@letsdrinkup.com'])
#         except BadHeaderError:
#             return HttpResponse('Invalid header found.')
#         return HttpResponse('Email sent')
#     else:
#         # In reality we'd use a form class
#         # to get proper validation errors.
#         return HttpResponse('Make sure all fields are entered and valid.')
