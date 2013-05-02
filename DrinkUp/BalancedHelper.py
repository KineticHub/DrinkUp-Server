import balanced
from django.conf import settings

class BalancedPaymentsHelper:

	def setupMarketplace(self):
		marketplace = balanced.configure(settings.BALANCED_API_KEY)
		if not balanced.Marketplace.my_marketplace:
			raise Exception("Marketplace.my_marketplace should not be nil")
		return marketplace
		
	def setupNewBankAccount(self, routing_number, account_number, account_type, name):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
			
		bank_account = balanced.BankAccount (
			    routing_number=routing_number,
			    account_number=account_number,
				type=account_type,
			    name=name,
			).save()
		
		return bank_account
		
	def setupNewMerchantAccount(self, bank_info, merchant_info, person_info):
	
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
			
		merchant_data = {
			    'phone_number': '+140899188155',
			    'name': 'Skripts4Kids',
			    'postal_code': '91111',
			    'type': 'business',
			    'street_address': '555 VoidMain Road',
			    'tax_id': '211111111',
			    'person': {
			        'phone_number': '+14089999999',
			        'dob': '1989-12',
			        'postal_code': '94110',
			        'name': 'Timmy Q. CopyPasta',
			        'street_address': '121 Skriptkid Row',
			    },
			}
			
		account = balanced.Account().save()

		try:
                        account.add_merchant(merchant_data)
                        bank_account = self.setupNewBankAccount(bank_info['routing_number'], bank_info['account_number'], bank_info['account_type'], bank_info['name'])
			account.add_bank_account(bank_account.uri)
			return account
		except balanced.exc.MoreInformationRequiredError as ex:
		    # could not identify this account.
		    print 'redirect merchant to:', ex.redirect_uri
		except balanced.exc.HTTPError as error:
		    # TODO: handle 400 and 409 exceptions as required
		    raise
		
	def setupNewCreditCard(self, card_number, expiration_month, expiration_year, security_code):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
			
		card = balanced.Card(
		    card_number=card_number,
		    expiration_month=expiration_month,
		    expiration_year=expiration_year,
			security_code=security_code
		).save()
		return card
		
	def addCreditCardToBuyer(self, account_uri, card_info):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
			
		account = balanced.Account.find(account_uri)
		card = self.setupNewCreditCard(card_info['card_number'], card_info['expiration_month'], card_info['expiration_year'], card_info['security_code'])
		account.add_card(card.uri)
		return account
	
	def setupNewBuyerAccount(self, username, email_address, card_uri=None):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
			
		account = balanced.Account(email_address=email_address, name=username).save()
		if card_uri is not None:
			account.add_card(card.uri)
		return account

	def debitBuyerCreditCard(self, account_uri, bar_name, amount, source_uri=None):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
			
		buyer = balanced.Account.find(account_uri)
		debit = buyer.debit(
		    appears_on_statement_as='DrinkUp - ' + bar_name,
		    amount=amount,
		    description= buyer.name + ' at ' + bar_name,
			source_uri=source_uri
		)
		return debit
		
	def addHoldDebitForBuyerCreditCard(self, account_uri, amount, source_uri=None):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()

		buyer = balanced.Account.find(account_uri)
		
		try:
			hold = buyer.hold(
			    amount=amount,
			    description= buyer.name + ' at ' + bar_name,
				source_uri=source_uri
			)
			return hold
		except balanced.exc.HTTPError as error:
			#if error.status_code == 402: 'insufficient funds'
			#error.category_code == 402:
			#canceled needs to be tested for status code if custom message to be used
			raise error
			
			#try:                                                    
			#...     account_test()                                      
			#... except balanced.exc.HTTPError as error:                 
			#...     print 'caught'                                      
			#...     print error.status_code
			
	def captureHoldDebitForBuyerCreditCard(self, hold_uri, bar_name):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
			
		hold = balanced.Hold.find(hold_uri)
		debit = hold.capture(
		    appears_on_statement_as='DrinkUp-' + bar_name,
		)
		
		return debit
		
	def voidHoldDebitForBuyerCreditCard(self, hold_uri, bar_name):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
			
		hold = balanced.Hold.find(hold_uri)
		hold.void(
			appears_on_statement_as='Voided: DrinkUp-' + bar_name,
		)
		
			
			
