import os
import datetime
import time
#from Transaction import *
from Block import block
from Blockchain_Util import *
import hashlib


class node:
    neigthbor = []
    public_key = ''
    def __init__(self):
        self.blockchain = []

    def generate_key():
        return 
    def mining(self, transactions):
        difficulty = utils.get_difficulty()
        zerostr = ''
        zerostr = zerostr.rjust(difficulty, '0')
        nonce = 0
        print zerostr
        print difficulty
        time_stamp = time.time()
        prev_hash = self.blockchain[-1].calculate_hash()
        print(prev_hash)
        newblock = block(difficulty, time_stamp, transactions, prev_hash, nonce)
        hash_val = newblock.calculate_hash()
        bin_hash_val = ( bin(int(hash_val, 16))[2:] ).zfill(256)
        print(bin_hash_val[:difficulty])
        while bin_hash_val[:difficulty] != zerostr:
            nonce += 1
            newblock = block(difficulty, time_stamp, transactions, prev_hash, nonce)
            hash_val = newblock.calculate_hash()
            bin_hash_val = ( bin(int(hash_val, 16))[2:] ).zfill(256)
        print(bin_hash_val)
        return newblock


        
    def transfer(to_address, amount):
        trans = transaction(self.address, to_address, amount)
        trans.sign(self.key)
        return trans
    
    def gossipl():
        return
    '''zhiyang lin'''
    def get_blance():
        total_balance = 0
        for block in self.blockchain:
            for transaction in block.transactions:
                if transaction.from_address == self.public_key:
                    total_balance -= transaction.amount
                if transaction.to_address == self.public_key:
                    total_balance += transaction.amount
        return total_balance