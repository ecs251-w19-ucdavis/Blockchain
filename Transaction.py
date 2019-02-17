# import DIFFICULTY from __init__
# import VERSION from __init__
import Queue
import time

class transaction:
	def __init__(self, from_address, to_address, amount):
		self.from_address = from_address
		self.to_address = to_address
		self.amount = amount
		self.timestamp = time.timestamp



	def isvalid(self):
		# check if the sign is valid
		# check if the amount is less than the money of the from_adress

		return True


	def create_transaction_pool(self):
		# create a global Queue
		transaction_pool = Queue.Queue(maxsize = 0)
		return transaction_pool


	def sign(self):
		# digital signiture 

		return True



	def __str__(self):
		information = "#Time: "+self.timestamp+"#  transaciton from "+self.from_address+" to "+self.to_addresss+"  with amount: "+ self.amount
		return information