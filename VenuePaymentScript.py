#! Python Payment Script

#model imports
from VenueApp.models import *
from BarApp.models import *
from UsersApp.models import *

#BalancedPayments
from DrinkUp.BalancedHelper import BalancedPaymentsHelper

helper = BalancedPaymentsHelper()

venues = Venue.objects.all()
orders = BarOrder.objects.filter(current_status=4, payment_processed=False)

for venue in venues:
    venue_total = 0
    for order in orders:
        amount = int(round(float(order.grand_total), 2)*100) - 5
        venue_total += amount
        
    merchant_account = balanced.Account.find(venue.bp_merchant)
    merchant_account.bank_accounts[0].credit(amount=venue_total)
