from decimal import Decimal
import json
from VenueApp.models import *
from BarApp.models import *

__author__ = 'Kinetic'

def calculateOrder(user_order):
    if user_order['appuser'] and user_order['bar_id'] and user_order['tip_percent'] and user_order['drinks']:
        bar = VenueBar.objects.get(pk=user_order['bar_id'])
        drinks_data = json.loads(user_order['drinks'])
        drink_total = 0.0
        is_happy_hour = bar.happyhour_start < datetime.now().time() < bar.happyhour_end
        for drink in drinks_data:
            price = Decimal(drink['price'])
            if is_happy_hour:
                price = Decimal(drink['happyhour_price'])
            drink_total += price * Decimal(drink['quantity'])
        sub_total = drink_total
        tip = Decimal(user_order['tip_percent']) * sub_total
        grand_total = total = sub_total + tip
        return {'appuser':user_order['appuser'],
                'bar_id':user_order['bar_id'],
                'drinks':user_order['drinks'],
                'tip_percent':user_order['tip_percent'],
                'drink_total':drink_total,
                'is_happyhour':is_happy_hour,
                'subtotal':sub_total,
                'tip':tip,
                'total':total,
                'grand_total':grand_total
        }

def createNewOrder(user_order):
    if user_order['appuser'] and user_order['bar_id'] and user_order['tip_percent'] and user_order['drinks']\
        and user_order['drink_total'] and user_order['is_happyhour'] and user_order['subtotal'] and user_order['tip'] \
        and user_order['total'] and user_order['grand_total']:
        primary_user = 1
        bar = VenueBar.objects.get(pk=user_order['bar_id'])
        drinks_data = json.loads(user_order['drinks'])

        new_order = BarOrder(user_id=primary_user,
                             venue=bar.venue,
                             bar=bar,
                             venue_name=bar.venue.name,
                             appuser=user_order['appuser'],
                             total=user_order['total'],
                             tax=0.0,
                             sub_total=user_order['subtotal'],
                             tip=user_order['tip'],
                             fees=0.0,
                             grand_total=user_order['grand_total'],
                             current_status=1,
                             description='')
        new_order.save()

        for drink in drinks_data:
            drink_type = VenueDrinkType.objects.get(pk=int(drink['drink_type']))
            price = Decimal(drink['price'])
            is_happyhour = bool(user_order['is_happyhour'])
            if is_happyhour:
                price = Decimal(drink['happyhour_price'])
            new_drink_ordered = BarDrinkOrdered(order=new_order, drink_name=drink['name'],
                                                quantity=int(drink['quantity']), unit_price=price,
                                                drink_type=drink_type.name, ordered_during_happyhour=is_happyhour)
            new_drink_ordered.save()

        return new_order