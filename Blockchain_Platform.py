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
    address_list = []
    mining_difficulty = [15]
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
                for user_info in self.registered_users:
                    if address == json.loads(user_info)['address']:
                        print(address + ' is already registered')
                        print(user_info)
                        return user_info
                print(address)
                pk, sk = self.generate_key()
                neighbors = self.assign_nbrs()
                user_info = json.dumps({'status':'success',
                                        'address':address,
                                        'private_key':sk,
                                        'public_key':pk,
                                        'neighbors':neighbors
                                        })
                new_node = json.dumps({'address':address,
                                        'public_key':pk
                                        })
                self.registered_users.append(user_info)
                self.address_list.append(new_node)
                return user_info

            # if action == 'print':
            #     print(json.dumps(self.registered_users))
            #     return json.dumps(self.registered_users)
            if action == 'update_difficulty':
                self.update_mining_difficulty(4)
                return str(self.mining_difficulty[0])

            if action == 'get_difficulty':
                print(self.mining_difficulty[0])
                return str(self.mining_difficulty[0])

            if action == 'get_firstblock':
                return str(self.create_genesis_block())

            if action == 'get_registered_users':
                return json.dumps(self.registered_users)
            
            if action == 'get_user_count':
                print(len(self.registered_users))
                return str(len(self.registered_users))

    def create_genesis_block(self):
        creation_date = time.mktime(datetime.datetime.strptime(self.chain_creation_date, "%d/%m/%Y").timetuple())
        return block(self.mining_difficulty, creation_date, [], 'this is the first block', 0)

    def update_mining_reward(self, blockchain):
        if len(blockchain) % 2100 == 0:
            self.mining_reward /= 2

    def update_mining_difficulty(self, new_difficulty):
        self.mining_difficulty[0] = new_difficulty


    def assign_nbrs(self):
        l = []
        user_num = len(self.address_list)
        if user_num == 0:
            return []
        elif user_num <= 2:
            return self.address_list
        elif user_num < 10:
            s = set()
            n = user_num/3
            while len(s) < n:
                s.add(random.randint(0,user_num - 1))
            for x in s:
                l.append(self.address_list[x])
            return l
        else:
            s = set()
            n = random.randint(1, user_num/3)
            while len(s) < n:
                s.add(random.randint(0,user_num - 1))
            for x in s:
                l.append(self.address_list[x])
            return l
    
    def generate_key(self):
        key = RSA.generate(2048) 
        pk = key.publickey().exportKey("PEM") 
        sk = key.exportKey("PEM") 
        return pk, sk