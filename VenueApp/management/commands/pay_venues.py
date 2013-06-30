from django.core.management.base import BaseCommand, CommandError

import warnings

#python imports
from datetime import datetime
from time import gmtime, strftime

#model imports
from VenueApp.models import *
from BarApp.models import *
from UsersApp.models import *

#BalancedPayments
import balanced
from django.conf import settings
#from DrinkUp.BalancedHelper import BalancedPaymentsHelper

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

class Command(BaseCommand):
    
    help = 'Pays out to the venues any open orders'

    def handle(self, *args, **options):

        self.stdout.write('Payments for day: %r\n\n' %  strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        
        #helper = BalancedPaymentsHelper()
        balanced.configure(settings.BALANCED_API_KEY)
        
        venues = Venue.objects.all()

        for venue in venues:
            venue_total = 0
            orders = BarOrder.objects.filter(venue=venue, current_status=4, payment_processed=True, venue_payment_processed=False)
            for order in orders:
                amount = int(round(float(order.grand_total), 2)*100) - 5
                venue_total += amount

                order.venue_payment_processed=True
                order.save()

            if venue_total > 0:
                merchant_account = balanced.Account.find(venue.bp_merchant)
                merchant_account.credit(amount=venue_total)
                
                #helper.payVenueMerchantAccount(venue=venue, amount=venue_total)

                self.stdout.write('Successfully paid %r a total of %r on %r\n' % (venue.name, venue_total, strftime("%Y-%m-%d %H:%M:%S", gmtime())))
            
        self.stdout.write('\n-----------------------------------\n\n')
