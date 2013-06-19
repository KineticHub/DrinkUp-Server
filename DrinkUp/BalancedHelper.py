import balanced
from django.conf import settings

class BalancedPaymentsHelper:

	def __init__(self):
			balanced.configure(settings.BALANCED_API_KEY_TEST)
			if not balanced.Marketplace.my_marketplace:
				raise Exception("Marketplace.my_marketplace should not be nil")

	def setupMarketplace(self):
		balanced.configure(settings.BALANCED_API_KEY_TEST)
		if not balanced.Marketplace.my_marketplace:
			raise Exception("Marketplace.my_marketplace should not be nil")
		return balanced.Marketplace.my_marketplace
		
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
		
	def setupNewMerchantAccount(self, merchant, person):
	
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
			
		merchant_data = {
				'phone_number': merchant.contact_number,
							'email_address': merchant.contact_email,
				'name': merchant.name,
				'postal_code': merchant.postal_code,
				'street_address': merchant.street_address,
				'tax_id': merchant.tax_id,
							'type': 'business',
				'person': {
									'phone_number': person.phone_number,
									'name': person.get_full_name(),
									'dob': person.dob.strftime('%Y-%m-%d'),
									'postal_code': person.postal_code,
									'street_address': person.street_address,
									'type': 'person',
				},
			}
			
		account = balanced.Account().save()

		try:
			account.add_merchant(merchant_data)
			return account
		except balanced.exc.MoreInformationRequiredError as ex:
			# could not identify this account.
			print 'redirect merchant to:', ex.redirect_uri
		except balanced.exc.HTTPError as error:
			# TODO: handle 400 and 409 exceptions as required
			raise
			
	def addMerchantBankAccount(self, merchant, bank):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
		
		account = balanced.Account.find(merchant.bp_merchant)
		bank_account = self.setupNewBankAccount(bank.routing_number, bank.account_number, bank.account_type, bank.bank_name)
		account.add_bank_account(bank_account.uri)
		return bank_account

##	def payVenueMerchantAccount(self, venue, amount):
##                if not balanced.Marketplace.my_marketplace:
##			self.setupMarketplace()
##			
##                merchant_account = balanced.Account.find(venue.bp_merchant)
##                #merchant_account.bank_accounts[0].credit(amount=amount)
##                #merchant_account.credit(amount=amount)
##                try:
##                    merchant_account.credit(amount=amount)
##                except AttributeError, e:
##                    print e
##                    import pdb
##                    pdb.set_trace()
		
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
			
		account = balanced.Customer.find(account_uri)
		card = self.setupNewCreditCard(card_info['card_number'], card_info['expiration_month'], card_info['expiration_year'], card_info['security_code'])
		account.add_card(card.uri)
		return account

	def updateBuyerCreditCard(self, cc_uri, account_uri):
                account = balanced.Customer.find(account_uri)
                for card in account.cards:
                        card.is_valid=False
                        card.save()
                account.add_card(cc_uri)
                return self.getBuyerCreditCardInfo(account_uri)

        def getBuyerCreditCardInfo(self, account_uri):
                account = balanced.Customer.find(account_uri)
                valid_card = None
                for card in account.cards:
                        if card.is_valid == True:
                                valid_card = card
                return valid_card

        def invalidateBuyerCreditCard(self, account_uri):
                account = balanced.Customer.find(account_uri)
                for card in account.cards:
                        card.is_valid=False
                        card.save()
	
	def setupNewBuyerAccount(self, username, email_address, card_uri=None):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
			
		customer = balanced.Customer(email_address=email_address, name=username).save()
		if card_uri is not None:
			account.add_card(card.uri)
		return customer

	def debitBuyerCreditCard(self, account_uri, bar_name, amount, source_uri=None):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
			
		buyer = balanced.Customer.find(account_uri)
		debit = buyer.debit(
			appears_on_statement_as='DrinkUp - ' + bar_name,
			amount=amount,
			description= buyer.name + ' at ' + bar_name,
			source_uri=source_uri
		)
		return debit
		
	def createHoldForOrder(self, account, order, source_uri=None):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()

		buyer = balanced.Customer.find(account.bp_account)
		
		try:
			hold = balanced.Hold(
				amount=int(round(float(order.grand_total), 2)*100), #this needs to be in pennies
				description= buyer.name + ' at ' + order.bar.venue.name,
				source_uri=buyer.cards[0].uri,
			).save()
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
			
	def captureHoldForOrder(self, order):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
		appears = 'DrinkUp ' + order.bar.venue.name
		hold = balanced.Hold.find(order.bp_transaction)
		debit = hold.capture(
			appears_on_statement_as= appears[:21]
		)
		
                #amount = int(round(float(order.grand_total), 2)*100) - 5
                #merchant_account = balanced.Account.find(order.venue.bp_merchant)
		#merchant_account.bank_accounts[0].credit(amount=amount)

		#balanced.Marketplace.my_marketplace.owner_account.credit(amount=your_fee)
		
		return debit
		
	def voidHoldForOrder(self, order):
		if not balanced.Marketplace.my_marketplace:
			self.setupMarketplace()
		appears = 'DrinkUp ' + order.bar.venue.name
		hold = balanced.Hold.find(order.bp_transaction)
		hold.void()
			
			
