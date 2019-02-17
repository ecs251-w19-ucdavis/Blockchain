from Block import block
import time
import datetime

class blockchain:
    mining_difficulty = 2
    mining_reward = 50
    chain_creation_date = "02/10/2019"
    @staticmethod
    def create_genesis_block():
        creation_date = time.mktime(datetime.datetime.strptime(blockchain.chain_creation_date, "%d/%m/%Y").timetuple())
        return block(blockchain.mining_difficulty, creation_date, [], 'this is the first block', 0)
    @staticmethod
    def set_mining_reward(self, len):
        if len % 2100 == 0:
            self.mining_reward /= 2
    @staticmethod
    def set_mining_difficulty(self, new_difficulty):
        self.mining_difficulty = new_difficulty