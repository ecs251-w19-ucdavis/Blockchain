# import DIFFICULTY from __init__
# import VERSION from __init__
import hashlib
import time
class block:
    def __init__(self, diffculty, time_stamp, transactions, prev_hash, Nonce, current_hash):
        self.difficulty = diffculty
        self.time_stamp = time_stamp
        self.transactions = transactions
        self.Nonce = Nonce
        self.prev_hash = prev_hash
        self.current_hash = calculate_hash()

    def __str__(self):
        str = str(self.time_stamp) + str(self.difficulty) + str(self.Nonce) + self.prev_hash 
        for transaction in transactions:
            str += transaction
        return str

    def calculate_hash():
        hash_val = haslib.sha256(str(self)).hexdigest()
        return hash_val

    def has_valid_transactions(self):
        for transaction in self.transactions:
            if not transaction.isvalid():
                return false
        return true

    


