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
from flask import jsonify

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
                return user_info

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