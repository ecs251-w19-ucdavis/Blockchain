# import DIFFICULTY from __init__
# import VERSION from __init__
# pycrypto
import Queue
import time
import json
import hashlib
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

class transaction:

	def __init__(self, from_address, to_address, amount, fee):
		self.from_address = from_address
		self.to_address = to_address
		self.amount = amount
		self.timestamp = time.time()
		self.fee = fee

	def isvalid(self, blockchain):
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
		if verify(msg_hash,self.my_sign):
			is_sign_valid = True

		# check if the amount is less than the money of the from_adress
		amount = 0
		for block in blockchain:
			for tx in block:
				if tx.from_address == self.from_address:
					amount -= tx.amount
				elif tx.from_address == self.to_address:
					amount += tx.amount
		if amount == self.amount:
			is_amount_valid == True
		if is_sign_valid and is_amount_valid:
			return True

		return False



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

	def __cmp__(self, other):
        	return cmp(self.fee, other.fee)

