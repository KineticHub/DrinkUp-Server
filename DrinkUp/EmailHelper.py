__author__ = 'Kinetic'

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
