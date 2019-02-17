# import DIFFICULTY from __init__
# import VERSION from __init__
import hashlib
import time
class block:
    def __init__(self, diffculty, time_stamp, transactions, prev_hash, Nonce):
        self.difficulty = diffculty
        self.time_stamp = time_stamp
        self.transactions = transactions
        self.Nonce = Nonce
        self.prev_hash = prev_hash
        self.current_hash = self.calculate_hash()

    def __str__(self):
        block_str = str(self.time_stamp) + str(self.difficulty) + str(self.Nonce) + self.prev_hash 
        for transaction in self.transactions:
            block_str += transaction
        print(block_str)
        return block_str

    def calculate_hash(self):
        hash_val = hashlib.sha256(self.__str__()).hexdigest()
        return hash_val

    def has_valid_transactions(self):
        for transaction in self.transactions:
            if not transaction.isvalid():
                return false
        return true

    


