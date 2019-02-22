from Block import block
import time
import datetime
import random
import json
from scipy import stats
import numpy as np

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

    def add_transaction(self, transaction):
        self.transaction_pool.append(transaction)

    def pick_transactions(self):
        tx_inds = []
        while len(tx_inds) < 10:
            tx_ind = random.randint(0,10)
            if tx_ind not in tx_inds:
                tx_inds.append(tx_ind)
        tx_list = []
        for tx_ind in tx_inds:
            tx_list.append(self.transaction_pool[tx_ind])
        return tx_list


    def add_voters(self, voter_info):
        if len(self.voter_pool) >= 100:
            return False
        self.voter_pool.append(voter_info)

    def pick_voters(self):
        """

        """
        # lock voter_pool before we pick voters
        voter_str = json.dumps(self.voter_pool)
        voter_json = json.loads(voter_str)
        total = 0
        for voter in voter_json:
            total += voter_json[voter]
        voter_prob = []
        for voter in voter_json:
            voter_prob.append(voter_json[voter]/total)
        index = np.arange(len(self.voter_pool))
        voter_cdd_index = stats.rv_discrete(name = 'voters_cdd' ,values = (index,voter_prob))
        voters_cdd = self.voter_pool[voter_cdd_index]
        return voters_cdd


    def assign_nbrs(self):
        return

    def generate_key(self):
        return






