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

client_port = 0
class node(flask.views.MethodView):
    neigthbor = []
    ip_address = 0
    public_key = ''
    private_key = ''
    blockchain = []
    tx_pool = []
    vote_pool = []
    new_block_pool = []
    can_add_vote = True
    def get(self):
        if request.method == 'GET':
            action = flask.request.args.get('action')
            if action == 'register':
                keys = self.generate_key()
                return keys

    def generate_key(self):
        self.ip_address = app.config['port']
        # print('ip_address is ' + str(self.ip_address))
        args = {'action':'register', 'address':self.ip_address}
        r = requests.get('http://127.0.0.1:8000/blockchain_platform', params=args)
        if r.status_code == 200:
            return r.text

    def mining(self):
        """
        Mining a new block and broadcast it to all users 
        """
        # pick 10 transactions from local transaction pool based on the fee
        # digital signature is unique for different transactions
        # select 15 randomly , then pick 10 with most fee
        tx_dict = {}
        for item in self.tx_pool:
            tx_dict[item.signature] = item.fee
        sorted_tx = sorted(tx_dict.item(), lambda x: x[0],reverse = True)
        txs_sign = sorted_tx[:10][0]
        transactions = []
        for tx in tx_pool:
            if tx.signature in txs_sign:
                transactions.append(tx)
        #####################################

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
        
    def transfer(self,to_address, amount):
        trans = transaction(self.address, to_address, amount)
        trans.sign(self.key)
        return trans


    def get_balance(self, address = self.public_key):
        total_balance = 0
        for block in self.blockchain:
            for transaction in block.transactions:
                if transaction.from_address == address:
                    total_balance -= transaction.amount
                if transaction.to_address == address:
                    total_balance += transaction.amount
        return total_balance


    def add_tx_to_pool(self,tx_str):
        """
        when receive a new transaction json format from the net, 
        build a transaction object and add it to the local tx_pool
        # using priority queeue
        """
        tx_json = json.loads(tx_str)
        tx = transaction(tx_json["from_address"],tx_json["to_address"],tx_json["amount"],tx_json["fee"])
        tx_pool.append(tx)

    def add_block_pool(self, newblock):
        """
        receive a new block from the net and create a new block object before add it to the block_pool
        """
        newblock = json.loads(newblock)
        new_block = block(newblock["difficulty"], newblock["time_stamp"], newblock["transactions"], newblock["prev_hash"], newblock["Nonce"])
        self.new_block_pool.append(new_block)




    def leader(self):

        return True


        

class vote:
    def __init__(self, from_address, blockhash, stake ):
        self.from_address = from_address
        self.blockhash = blockhash
        self.stake = stake


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
