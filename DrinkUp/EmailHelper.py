__author__ = 'Kinetic'

from django.conf import settings
from django import template
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage

from DrinkUp.BalancedHelper import BalancedPaymentsHelper


def send_email_to_user (email_args):

	user_emails = [email_args['user'].email]
	subject = email_args['subject']
	content = email_args['content']
	html_content = email_args['html_content']

	msg = EmailMultiAlternatives(
		subject=subject,
		body=content,
		from_email=settings.EMAIL_SENDER_PREFIX + "<team@letsdrinkup.com>",
		to=user_emails,
		headers={'Reply-To': "Support <k.alnajar@letsdrinkup.com>"} # optional extra headers
	)
	msg.attach_alternative(html_content, "text/html")

	# Optional Mandrill-specific extensions:
	#msg.tags = ["one tag", "two tag", "red tag", "blue tag"]
	msg.metadata = {'user_id': email_args['user'].pk, 'user_name': email_args['user'].username}

	# Send it:
	msg.send()


def send_order_receipt_email (order):
	from BarApp.models import BarDrinkOrdered, BarOrder

	html_email = ''
	with open(settings.SETTINGS_PATH + "/resources/user_receipt.html", "r") as receipt_html:
		html_email = receipt_html.read().replace('\n', '')

	receipt_template = template.Template(html_email)
	drinks_ordered = BarDrinkOrdered.objects.filter(order=order)
	helper = BalancedPaymentsHelper()
	card = helper.getBuyerCreditCardInfo(account_uri=order.appuser.bp_account)

	receipt_context = template.Context({'order': order, 'drinks_list':drinks_ordered, 'card':card})

	email_args = {'user': order.appuser.user,
	              'subject': 'Your receipt for order {order_id}'.format(order_id=order.pk),
	              'content': 'This is where the order information will be given.',
	              'html_content': receipt_template.render(receipt_context)}
	send_email_to_user(email_args)
