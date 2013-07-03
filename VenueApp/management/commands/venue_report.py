import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")


class Command(BaseCommand):

    from django.core.management.base import BaseCommand, CommandError

    #python imports
    from datetime import datetime, timedelta
    from time import gmtime, strftime
    import warnings
    import csv

    #model imports
    from VenueApp.models import *
    from BarApp.models import *
    from UsersApp.models import *

    #BalancedPayments
    import balanced
    from django.conf import settings
    #from DrinkUp.BalancedHelper import BalancedPaymentsHelper

    help = 'Sends a report to the venues of orders processed over the past day'

    def handle(self, *args, **options):
        self.stdout.write('Reports for day: %r\n\n' % strftime("%Y-%m-%d %H:%M:%S", gmtime()))

        venues = Venue.objects.all()
        for venue in venues:
            orders = BarOrder.objects.filter(venue=venue, created__gte=datetime.now() - timedelta(hours=24))
            report_title = '{venue_name}_{timestamp}.csv'.format(venue_name=venue.name, timestamp=datetime.now())
            report = csv.writer(open(report_title, "wb"))
            report.writerow(["Timestamp", "Order ID"])
            for order in orders:
                report.writerow([order.created, order.pk])

        self.stdout.write('\n-----------------------------------\n\n')