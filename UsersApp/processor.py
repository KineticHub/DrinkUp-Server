import pinject
from DrinkUp.Helpers.BalancedHelper import BalancedPaymentsHelper
from UsersApp.binding_specs import UsersAppBindingSpec
import UsersApp

__author__ = 'Kinetic'


class UsersAppProcessor(object):
    injector = pinject.new_object_graph(binding_specs=[UsersAppBindingSpec()])
    balanced_payments = injector.provide(BalancedPaymentsHelper)

    @classmethod
    def createNewBalancedPaymentsAccountForAppUser(cls, app_user):
        assert isinstance(app_user, UsersApp.models.AppUser), "createNewBalancedPaymentsAccountForAppUser requires an AppUser instance"
        new_account = cls.balanced_payments.setupNewBuyerAccount(username=app_user.user.username,
                                                                 email_address=app_user.user.email)
        return new_account.uri