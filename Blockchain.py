import Block
import time

class blockchain:
    def __init__(self)
        self.mining_difficulty = 2
        self.mining_reward = 50
    
    def create_genesis_block(self):
        return Block(self.mining_difficulty, time.timestamp(), [], '', 0)
    
    def set_mining_reward(self, len):
        if len % 2100 == 0:
            self.mining_reward /= 2
    
    def set_mining_difficulty():
        return