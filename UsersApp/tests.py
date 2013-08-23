"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import copy
from django.contrib.auth.models import User
from mock import MagicMock, Mock, patch
from django.test import TestCase
from UsersApp.models import AppUser


class UsersAppTest(TestCase):

    USERNAME = "JSmith"
    EMAIL = "john.smith@example.com"
    PASSWORD = "jspassword"
    FAKE_BP_ACCOUNT = "/v1/customers/CU5iqmskN3o9gyBmuthvFaqP"

    def test_create_User_lowercase_email_and_name(self):
        """
        Test that after User object is saved
        the name and email are saved in lowercase
        """
        uppercase_name = "JSMITH"
        lowercase_name = "jsmith"
        uppercase_email = "JSMITH@EXAMPLE.COM"
        lowercase_email = "jsmith@example.com"

        new_user = User.objects.create_user(username=uppercase_name, email=uppercase_email, password=self.PASSWORD)
        self.assertEqual(lowercase_name, new_user.username)
        self.assertEqual(lowercase_email, new_user.email)

    def test_create_new_AppUser(self):
        """
        Test creation of new AppUser
        """

        user = User.objects.create_user(username=self.USERNAME, email=self.EMAIL, password=self.PASSWORD)
        appuser = AppUser(user=user)
        users_app_processor = MagicMock()
        users_app_processor.createNewBalancedPaymentsAccountForAppUser = MagicMock(return_value=self.FAKE_BP_ACCOUNT)
        AppUser.users_app_processor = users_app_processor
        appuser.save()

        self.assertEqual(appuser.user.pk, user.pk, "appuser.user and user should be the same")
        self.assertEqual(appuser.bp_account, self.FAKE_BP_ACCOUNT, "appuser.bp_account should be fake account uri")

    def test_save_AppUser_with_existing_BP_account(self):
        """
        Test that an AppUser being updated keeps the same BalancedPayments
        account URI and does not get overwritten
        """

        user = User.objects.create_user(username=self.USERNAME, email=self.EMAIL, password=self.PASSWORD)
        appuser = AppUser(user=user)
        users_app_processor = MagicMock()
        users_app_processor.createNewBalancedPaymentsAccountForAppUser = MagicMock(return_value=self.FAKE_BP_ACCOUNT)
        AppUser.users_app_processor = users_app_processor
        appuser.save()

        self.assertEqual(users_app_processor.createNewBalancedPaymentsAccountForAppUser.call_count, 1,
                         "expected createNewBalancedPaymentsAccountForAppUser to only be called once")
        self.assertEqual(appuser.bp_account, self.FAKE_BP_ACCOUNT, "appuser.bp_account should be fake account uri")

        appuser.gender = 'male'
        appuser.save()
        self.assertEqual(users_app_processor.createNewBalancedPaymentsAccountForAppUser.call_count, 1,
                         "createNewBalancedPaymentsAccountForAppUser should not be called again")
        self.assertEqual(appuser.bp_account, self.FAKE_BP_ACCOUNT,
                         "appuser.bp_account should not change after first save")

