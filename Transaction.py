# import DIFFICULTY from __init__
# import VERSION from __init__
# pycrypto
import Queue
import time
import json
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

class transaction:
	def __init__(self, from_address, to_address, amount,sk):
		self.from_address = from_address
		self.to_address = to_address
		self.amount = amount
		self.timestamp = time.time()


	def isvalid(self,my_sign):
		'''
		arg: signed message
		return: are the signature and the amount valid
		'''

		# check if the sign is valid
		is_sign_valid = False
		is_amount_valid = False
		msg = str(self)
		msg_hash = SHA256.new()
		msg_hash.update(msg)
		verify = PKCS1_PSS.new(self.from_address)
		if verify(msg_hash,my_sign):
			is_sign_valid = True

		# check if the amount is less than the money of the from_adress


		if :
			is_amount_valid = True


		if is_sign_valid and is_amount_valid:
			return True

		return False


	# def create_transaction_pool(self):
	# 	# Initialize a global Queue
	# 	transaction_pool = Queue.Queue(maxsize = 0)
	# 	return transaction_pool


	def sign(self,sk):
		''' 
		arg: secret key
		return: signiture of this transaction
		'''

		#compute the checksum of the transaction message
		msg_hash = SHA256.new()
		msg_hash.update(str(self))

		#sign the message with the private key
		signature = PKCS1_PSS.new(self.from_address)
		my_sign = signature.sign(msg_hash)
		self.signature = my_sign
		print("my signature is", my_sign)
		return my_sign
	


	def __str__(self):
		tx = json.dumps(self,default=lambda x: x.__dict__)
		return tx



