from Block import block
import time
import datetime
import random
import json
#from scipy import stats
import os
import numpy as np
from Crypto.PublicKey import RSA
import flask
from flask import redirect, request, views


class blockchain_platform(flask.views.MethodView):
    transaction_pool = []
    registered_users = []
    new_block_pool = []
    voter_pool = []
    mining_difficulty = 2
    mining_reward = 50
    chain_creation_date = "02/10/2019"
    def get(self):
        if request.method == 'GET':
            action = flask.request.args.get('action')
            if action == None or action == "":
                return "Please specify an action"
            print("action " + action)
            if action == 'register':
                address = flask.request.args.get('address')
                print(address)
                pk, sk = self.generate_key()
                neighbors = self.assign_nbrs()
                user_info = json.dumps({'status':'success',
                                        'address':address,
                                        'secretkey':sk,
                                        'publickey':pk,
                                        'neighbor':neighbors
                                        })
                new_node = json.dumps({'address':address,
                                        'publickey':pk
                                        })
                self.registered_users.append(new_node)
                return(user_info)

            if action == 'print':
                return str(self.registered_users)
        

    def create_genesis_block(self):
        creation_date = time.mktime(datetime.datetime.strptime(self.chain_creation_date, "%d/%m/%Y").timetuple())
        return block(self.mining_difficulty, creation_date, [], 'this is the first block', 0)

    def update_mining_reward(self, blockchain):
        if len(blockchain) % 2100 == 0:
            self.mining_reward /= 2

    def update_mining_difficulty(self, new_difficulty):
        self.mining_difficulty = new_difficulty

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
        voter_cdd_index = np.random.choice(index, p = voter_prob, size = 10, replace = True)
        voters_cdd = self.voter_pool[voter_cdd_index]
        return voters_cdd


    def assign_nbrs(self):
        if len(self.registered_users) == 0:
            return 

    def generate_key(self):
        """
        rtype: pk public key
        rtype: sk secret key
        """
        key = RSA.generate(2048) 
        pk = key.publickey().exportKey("PEM") 
        sk = key.exportKey("PEM") 
        return pk, sk