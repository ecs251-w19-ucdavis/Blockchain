# import DIFFICULTY from __init__
# import VERSION from __init__
import hashlib
import time
import json
class block:
    def __init__(self, diffculty, time_stamp, transactions, prev_hash, Nonce):
        self.difficulty = diffculty
        self.time_stamp = time_stamp
        self.transactions = transactions
        self.Nonce = Nonce
        self.prev_hash = prev_hash
        self.current_hash = self.calculate_hash()

    def __str__(self):
        block_str = json.dumps(self, default=lambda o: o.__dict__)
        # print(test_str)
        return block_str

    def calculate_hash(self):
        data = {}
        data['Difficulty'] = self.difficulty
        data['Time_Stamp'] = self.time_stamp
        data['Transactions'] = self.transactions
        data['Nonce'] = self.Nonce
        data['Prev_hash'] = self.prev_hash
        json_data = json.dumps(data)
        hash_val = hashlib.sha256(json_data).hexdigest()
        self.current_hash = hash_val
        return hash_val

    def has_valid_transactions(self):
        for transaction in self.transactions:
            if not transaction.isvalid():
                return false
        return true

    


