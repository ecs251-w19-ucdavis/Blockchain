import os
import datetime
import time
#from Transaction import *
from Block import block
import hashlib
import requests
import sys
import re
import flask
from flask import Flask
from flask import redirect, request, views
from flask import Response
import json
from Transaction import transaction
import Queue
import random

client_port = 0
class node(flask.views.MethodView):
    neighbors = []
    ip_address = 0
    public_key = [None]
    private_key = [None]
    blockchain = []
    tx_pool = []
    vote_pool = []
    new_block_pool = []
    state = [None]
    
    def get(self):
        if request.method == 'GET':
            action = flask.request.args.get('action')
            if action == 'register':
                keys = self.register()
                self.blockchain.append(self.get_firstblock())

                return keys

            if action == 'getkeys':
                print('getting keys')
                if self.public_key == []:
                    return 'no keys'
                else:
                    print('ipaddress' + str(app.config['port']))
                    return self.public_key[0]

            if action == 'transfer':
                from_address = self.ip_address
                to_address = flask.request.args.get('to_address')
                timestamp = time.time()
                amount = flask.request.args.get('amount')
                fee = flask.request.args.get('fee')
                new_tx = transaction(timestamp, app.config['port'], to_address, amount, fee)
                self.tx_pool.append(str(new_tx))
                self.transfer(str(new_tx))
                print('called transfer')
                return str(new_tx)


            if action == 'gossip_transaction':
                tx = flask.request.args.get('transaction')
                # tx_json = json.loads(tx_str)
                # tx = transaction(tx_json["timestamp"], tx_json["from_address"], tx_json["to_address"], tx_json["amount"], tx_json["fee"])
                if tx in self.tx_pool:
                    print('Already has that transaction')
                    return 'Already has that transaction'
                else:
                    self.tx_pool.append(str(tx))
                    self.transfer(str(tx))
                    print(tx + ' has been added to the transaction pool. Sending it to neighbors')
                    return tx + ' has been added to the transaction pool. Sending it to neighbors'
            if action == 'gossip_blcok':
                
            if action == 'add_neighbor':
                neighbor = flask.request.args.get('neighbor')
                self.neighbors.append(neighbor)
                return 'Successfully add neighbor'

            if action == 'show_neighbors':
                for neighbor in self.neighbors:
                    # print(neighbor)
                    neighbor = json.loads(neighbor)
                    print('neighbor address ' + str(neighbor['address']))
                    print('-----')
                return 'showing neighbors'
                
            if action == 'show_transactions':
                for tx in self.tx_pool:
                    print(tx)
                return json.dumps(self.tx_pool)
            
            if action == 'start_mining':
                result = self.mining()
                return result
            
            if action == 'show_blocks':
                for block in self.blockchain:
                    print(block)
                return json.dumps(self.blockchain)

    def register(self):
        self.ip_address = app.config['port']
        # print('ip_address is ' + str(self.ip_address))
        args = {'action':'register', 'address':self.ip_address}
        r = requests.get('http://127.0.0.1:8000/blockchain_platform', params=args)
        if r.status_code == 200:
            keys = json.loads(r.text)
            self.public_key[0] = keys['public_key']
            self.private_key[0] = keys['private_key']
            # print('this is private key' + self.private_key[0])
            for neighbor in keys['neighbors']:
                print(neighbor)
                self.neighbors.append(neighbor)
                neighbor = json.loads(neighbor)
                print(neighbor['address'])
                self.inform(neighbor['address'])
            return r.text

    def mining(self):
        """
        Mining a new block and broadcast it to all users 
        """

        print('starting to mining')
        # pick 10 transactions from local transaction pool based on the fee
        # digital signature is unique for different transactions
        # select 15 randomly , then pick 10 with most fee
        transactions = []
        q = Queue.PriorityQueue()
        s = set()
        while len(s) < 6:
            s.add(random.randint(0,len(self.tx_pool) - 1))
        for x in s:
            q.put(self.tx_pool[x])
        while(len(transactions) < 5):
            transactions.append(q.get())

        

        # txs_sign = sorted_tx[:10][0]
        # transactions = []
        # for tx in self.tx_pool:
        #     if tx.signature in txs_sign:
        #         transactions.append(tx)
        #####################################

        difficulty = self.get_difficulty()
        print(difficulty)
        leading_zeros = ''
        leading_zeros = leading_zeros.rjust(difficulty, '0')
        nonce = 0
        print leading_zeros
        print difficulty
        time_stamp = time.time()
        prev_hash =self.block_json_to_obj(self.blockchain[-1]).calculate_hash()
        print(prev_hash)
        newblock = block(difficulty, time_stamp, transactions, prev_hash, nonce)
        hash_val = newblock.calculate_hash()
        bin_hash_val = ( bin(int(hash_val, 16))[2:] ).zfill(256)
        print(bin_hash_val[:difficulty])
        while bin_hash_val[:difficulty] != leading_zeros:
            nonce += 1
            newblock = block(difficulty, time_stamp, transactions, prev_hash, nonce)
            hash_val = newblock.calculate_hash()
            bin_hash_val = ( bin(int(hash_val, 16))[2:] ).zfill(256)
        print(bin_hash_val)
        return str(newblock)
        

    def transfer(self, new_tx):
        for neighbor in self.neighbors:
            print('neighbor')
            neighbor = json.loads(neighbor)
            print('neighbor address ' + str(neighbor['address']))
            args = {'action':'gossip_transaction', 'transaction':new_tx}
            url = 'http://127.0.0.1:' + str(neighbor['address']) + '/node'
            print('trying to gossip transaction ' + url)
            r = requests.get(url, params=args)
            print(r.text)
        return 'Making a transaction'

    def inform(self, address):
        selfinfo = json.dumps({'address':app.config['port'],
                                'public_key':self.private_key[0]
                                })
        args = {'action':'add_neighbor', 'neighbor':selfinfo}
        url = 'http://127.0.0.1:' + address + '/node'
        r = requests.get(url, params=args)
        print (r.text)
        return r.text

    def get_balance(self):
        total_balance = 0
        for block in self.blockchain:
            for transaction in block.transactions:
                if transaction.from_address == self.public_key[0]:
                    total_balance -= transaction.amount
                if transaction.to_address == self.public_key[0]:
                    total_balance += transaction.amount
        return total_balance

    def get_difficulty(self):
        args = {'action':'get_difficulty'}
        url = 'http://127.0.0.1:8000/blockchain_platform'
        r = requests.get(url, params=args)
        return int(r.text)
    
    def get_firstblock(self, ):
        args = {'action':'get_firstblock'}
        url = 'http://127.0.0.1:8000/blockchain_platform'
        r = requests.get(url, params=args)
        return r.text


    def tx_json_to_obj(self, tx_str):
        tx_json = json.loads(tx_str)
        tx = transaction(tx_json["from_address"], tx_json["to_address"], tx_json["amount"], tx_json["fee"])
        return tx

    def block_json_to_obj(self, newblock):
        """
        receive a new block from the net and create a new block object before add it to the block_pool
        """
        newblock = json.loads(newblock)
        new_block = block(newblock["difficulty"], newblock["time_stamp"], newblock["transactions"], newblock["prev_hash"], newblock["Nonce"])
        return new_block

def create_app(client_port):
    app = Flask(__name__) #create the application instance
    app.config.from_object(__name__) #load onfig from this file
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['port'] = client_port
    templates_dir = os.path.join(os.path.basename(os.getcwd()), 'templates')
    #load default config and override config from an enviroment variable
    app.add_url_rule('/node',
                        view_func=node.as_view('%s/%s' % (templates_dir, 'index')),
                         methods=["GET", "POST"])
    app.secret_key = "aaw"
    return app




if __name__ == "__main__":
    client_port = int(sys.argv[1])
    print(client_port)
    print('\n [*] Start API Service on port: %s' % (client_port))
    app = create_app(client_port)
    app.run(host='0.0.0.0', port=client_port, threaded=True, debug=True, use_reloader=True)
