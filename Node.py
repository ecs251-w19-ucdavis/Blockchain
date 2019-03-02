import os
import datetime
import time
from Transaction import *
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

client_port = 0
class node(flask.views.MethodView):
    is_registered = False
    neighbors = []
    ip_address = []
    public_key = [None]
    private_key = [None]
    blockchain = []
    transaction_pool = []
    def get(self):
        if request.method == 'GET':
            action = flask.request.args.get('action')
            if action == 'register':
                if self.public_key[0] != None:
                    return 'It is already registerd'
                keys = self.generate_key()
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
                amount = flask.request.args.get('amount')
                new_tx = transaction(app.config['port'], to_address, amount)
                self.transaction_pool.append(str(new_tx))
                self.transfer(str(new_tx))
                print('called transfer')
                return str(new_tx)
                # self.transfer(new_tx)


            if action == 'gossip_transaction':
                content = flask.request.args.get('content')
                if content in self.transaction_pool:
                    print('Already has that transaction')
                    return 'Already has that transaction'
                else:
                    self.transaction_pool.append(content)
                    self.transfer(content)
                    print(content + ' has been added to the transaction pool. Sending it to neighbors')
                    return content + ' has been added to the transaction pool. Sending it to neighbors'
                # if item == 'block':
                #     if content in self.blockchain:
                #         print('has block')
                #     else:
                #         self.blockchain.append(content)



            if action == 'show_neighbors':
                for neighbor in self.neighbors:
                    # print(neighbor)
                    neighbor = json.loads(neighbor)
                    print('neighbor address ' + neighbor['address'])
                    print('-----')
                return 'showing neighbors'
            if action == 'show_transactions':
                for tx in self.transaction_pool:
                    print(tx)
                return str(self.transaction_pool)

    def generate_key(self):
        ip_address = app.config['port']
        # print('ip_address is ' + str(self.ip_address))
        args = {'action':'register', 'address':ip_address}
        r = requests.get('http://127.0.0.1:8000/blockchain_platform', params=args)
        if r.status_code == 200:
            self.is_registered = True 
            print(r.text)
            keys = json.loads(r.text)
            # self.keytup.append(self.keys['public_key'])
            # self.keytup.append(self.keys['private_key'])
            # print(keys['public_key'])
            # print(keys['private_key'])
            self.public_key[0] = keys['public_key']
            self.private_key[0] = keys['private_key']
            # print('this is private key' + self.private_key[0])
            for neighbor in keys['neighbors']:
                print(neighbor)
                self.neighbors.append(neighbor)
            # print(self.neighbors)
            return r.text

    def mining(self, transactions):
        difficulty = utils.get_difficulty()
        leading_zeros = ''
        leading_zeros = leading_zeros.rjust(difficulty, '0')
        nonce = 0
        print leading_zeros
        print difficulty
        time_stamp = time.time()
        prev_hash = self.blockchain[-1].calculate_hash()
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
        return newblock
    
    # def get_keys()
    def transfer(self, new_tx):
        print('inside transfer')
        for neighbor in self.neighbors:
            print('neighbor')
            neighbor = json.loads(neighbor)
            print('neighbor address ' + neighbor['address'])
            args = {'action':'gossip_transaction', 'content':new_tx}
            url = 'http://127.0.0.1:' + neighbor['address'] + '/node'
            print('trying to gossip transaction ' + url)
            r = requests.get(url, params=args)
            print(r.text)
        return 'Making a transaction'
    
    # def shown_neighbour(self):
    #     str =''
    #     for neighbor in self.neigthbors:
            
    # def gossip():
    #     return

    '''zhiyang lin'''
    def get_blance():
        total_balance = 0
        for block in self.blockchain:
            for transaction in block.transactions:
                if transaction.from_address == self.public_key:
                    total_balance -= transaction.amount
                if transaction.to_address == self.public_key:
                    total_balance += transaction.amount
        return total_balance



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
