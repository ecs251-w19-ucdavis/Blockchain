from Block import block
import time
import datetime
import random

class blockchain_platform:
    def __int__(self, difficulty, reward):
        self.transaction_pool = []
        self.new_block_pool = []
        self.voter_pool = []
        self.mining_difficulty = difficulty
        self.mining_reward = reward
        self.chain_creation_date = "02/10/2019"

    def create_genesis_block(self):
        creation_date = time.mktime(datetime.datetime.strptime(self.chain_creation_date, "%d/%m/%Y").timetuple())
        return block(self.mining_difficulty, creation_date, [], 'this is the first block', 0)

    def update_mining_reward(self, blockchain):
        if len(blockchain) % 2100 == 0:
            self.mining_reward /= 2

    def update_mining_difficulty(self, new_difficulty):
        self.mining_difficulty = new_difficulty

    def get_transaction(self):
        tx_inds = []
        while len(tx_inds) < 10:
            tx_ind = random.randint(0,10)
            if tx_ind not in tx_inds:
                tx_inds.append(tx_ind)
        tx_list = []
        for tx_ind in tx_inds:
            tx_list.append(self.transaction_pool[tx_ind])
        return tx_list
        """

        """


    def new_block_pool():
        """

        """

    def voter_pool():
        """

        """

    def voter_pick():
        """
        get all legal 

        """
