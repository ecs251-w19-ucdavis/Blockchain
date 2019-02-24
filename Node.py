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

client_port = 0
class node(flask.views.MethodView):
    neigthbor = []
    ip_address = 0
    public_key = ''
    private_key = ''
    blockchain = []
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
        
    def transfer(to_address, amount):
        trans = transaction(self.address, to_address, amount)
        trans.sign(self.key)
        return trans
    
    # def gossipl():
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
