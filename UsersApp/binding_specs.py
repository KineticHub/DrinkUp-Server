import pinject
from DrinkUp.Helpers.BalancedHelper import BalancedPaymentsHelper

__author__ = 'Kinetic'

class UsersAppBindingSpec(pinject.BindingSpec):
    def configure(self, bind):
        bind('balanced_payments', to_class=BalancedPaymentsHelper)