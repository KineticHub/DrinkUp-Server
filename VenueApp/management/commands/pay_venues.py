from django.core.management.base import BaseCommand, CommandError

#python imports
from datetime import datetime
from time import gmtime, strftime

#model imports
from VenueApp.models import *
from BarApp.models import *
from UsersApp.models import *

#BalancedPayments
from DrinkUp.BalancedHelper import BalancedPaymentsHelper

class Command(BaseCommand):
    
    help = 'Pays out to the venues any open orders'

    def handle(self, *args, **options):
        
        helper = BalancedPaymentsHelper()
        venues = Venue.objects.all()
        orders = BarOrder.objects.filter(current_status=4, payment_processed=True, venue_payment_processed=False)

        for venue in venues:
            venue_total = 0
            for order in orders:
                amount = int(round(float(order.grand_total), 2)*100) - 5
                venue_total += amount

                order.venue_payment_processed=True
                order.save()

            if venue_total > 0:
                helper.payVenueMerchantAccount(venue=venue, amount=venue_total)

            self.stdout.write('Successfully paid %r a total of %r on %r\n' % (venue.name, venue_total, strftime("%Y-%m-%d %H:%M:%S", gmtime())))
            
        self.stdout.write('\n-----------------------------------\n\n')
