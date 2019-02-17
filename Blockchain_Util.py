from Block import block
import time
import datetime

class blockchain:
    def __init__(self):
        self.mining_difficulty = 2
        self.mining_reward = 50
        self.chain_creation_date = "02/10/2019"
    
    def create_genesis_block(self):
        creation_date = time.mktime(datetime.datetime.strptime(self.chain_creation_date, "%d/%m/%Y").timetuple())
        return block(self.mining_difficulty, creation_date, [], 'this is the first block', 0)
    
    def set_mining_reward(self, len):
        if len % 2100 == 0:
            self.mining_reward /= 2
    
    def set_mining_difficulty(self, new_difficulty):
        self.mining_difficulty = 2