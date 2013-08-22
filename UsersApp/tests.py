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

    def test_save_AppUser_with_existing_BP_account(self):
        """
        Test that an AppUser being updated keeps the same BalancedPayments
        account URI and does not get overwritten
        """

        FAKE_BP_ACCOUNT = "/v1/customers/CU5iqmskN3o9gyBmuthvFaqP"

        def changeBP(appuser):
            appuser.bp_account = FAKE_BP_ACCOUNT

        # user = User.objects.create_user(username=self.USERNAME, email=self.EMAIL, password=self.PASSWORD)
        # appuser = AppUser(user=user)
        # appuser.createAccount = Mock(side_effect=changeBP(appuser))
        # appuser.save()

        with patch.object(AppUser, 'createAccount', autospec=True) as mockCreateAccount:
            mockCreateAccount.return_value = FAKE_BP_ACCOUNT
            user = User.objects.create_user(username=self.USERNAME, email=self.EMAIL, password=self.PASSWORD)
            appuser = AppUser(user=user)
            appuser.createAccount = mockCreateAccount
            print "Account: " + appuser.bp_account
            appuser.save()
            print "Account: " + appuser.bp_account
