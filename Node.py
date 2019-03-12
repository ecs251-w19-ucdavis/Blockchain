import os
import datetime
import time
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
import threading 
from consutil import *

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
    leader = [None]
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
                from_address = app.config['port']
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
                if tx in self.tx_pool:
                    print('Already has that transaction')
                    return 'Already has that transaction'
                else:
                    self.tx_pool.append(str(tx))
                    self.transfer(str(tx))
                    print(tx + ' has been added to the transaction pool. Sending it to neighbors')
                    return tx + ' has been added to the transaction pool. Sending it to neighbors'

            if action == 'gossip_block':
                blockinfo = flask.request.args.get('block')
                block = json.loads(blockinfo)['block']
                block_obj = self.block_json_to_obj(block)
                if self.block_json_to_obj(self.blockchain[-1]).calculate_hash() != block_obj.prev_hash:
                    print('Block prev_hash not valid')
                    return 'Block prev_hash not valid'
                if blockinfo in self.new_block_pool:
                    print('Already has that block')
                    return 'Already has that block'
                else:
                    self.new_block_pool.append(str(blockinfo))
                    self.gossip_block(str(blockinfo))
                    if len(self.new_block_pool) == 3:
                        t = sys.maxint
                        for blockinfo in self.new_block_pool:
                            block = self.block_json_to_obj(json.loads(blockinfo)['block'])
                            if block.time_stamp < t:
                                t = block.time_stamp
                                address = json.loads(blockinfo)['address']
                                print(address)
                        if address == app.config['port']:
                            print(str(app.config['port']) + ' is the leader')
                            self.leader[0] = app.config['port']
                            self.announce_leader(app.config['port'])
                    return blockinfo + ' has been added to the transaction pool. Sending it to neighbors'

            if action == 'add_block':
                block_str = flask.request.args.get('block')
                block = self.block_json_to_obj(block_str)
                if self.block_json_to_obj(self.blockchain[-1]).calculate_hash() != block.prev_hash:
                    print('Block prev_hash not valid')
                    return 'Block prev_hash not valid'
                else:
                    self.blockchain.append(str(block))
                    res = str(block) + ' has been added to the blockchain of '+ str(app.config['port']) + ' Sending it to neighbors'
                    print(res)
                    self.add_block(str(block))
                    self.new_block_pool = []
                    return res

            if action == 'request_vote':
                leader_address = flask.request.args.get('leader')
                self.leader[0] = leader_address
                if self.state[0] == 'voted':
                    print("Already voted")
                    return "Already voted"
                else:
                    self.state[0] = 'voted'
                    self.vote(leader_address)
                    print("voting to " + leader_address)
                    self.announce_leader(leader_address)
                    return "voted"

            if action == 'send_vote':
                v = flask.request.args.get('vote')
                print('sending vote')
                self.vote_pool.append(v)
                if len(self.vote_pool) == 4:
                    blockhash = consutil.vote_sum(self.vote_pool)
                    print(blockhash)
                    for blockinfo in self.new_block_pool:
                        block = self.block_json_to_obj(json.loads(blockinfo)['block'])
                        if block.calculate_hash() == blockhash:
                            self.blockchain.append(str(block))
                            self.new_block_pool = []
                            self.add_block(str(block))
                return v

            if action == 'add_neighbor':
                neighbor = flask.request.args.get('neighbor')
                self.neighbors.append(neighbor)
                return 'Successfully add neighbor'

            if action == 'start_mining':
                new_block = self.mining()
                prev_hash = self.block_json_to_obj(self.blockchain[-1]).calculate_hash()
                if new_block.prev_hash != prev_hash:
                    return 'block void'
                address = app.config['port']
                new_block = json.dumps({'address' : address,
                          'block' : str(new_block)
                            })
                self.new_block_pool.append(new_block)
                self.gossip_block(str(new_block))
                return str(new_block)
            
            if action == 'show_blocks':
                blocks = []
                for block in self.new_block_pool:
                    block = json.loads(block)['block']
                    blocks.append(block)
                return json.dumps(blocks)

            if action == 'show_blockchain':
                return json.dumps(self.blockchain)

            if action == 'show_neighbors':
                neighbors = ''
                for neighbor in self.neighbors:
                    neighbor = json.loads(neighbor)
                    neighbors += ('neighbor address ' + str(neighbor['address']) +'\n')
                return neighbors
                
            if action == 'show_transactions':
                return json.dumps(self.tx_pool)

            if action == 'show_votes':
                return json.dumps(self.vote_pool)
            
            if action == 'show_leader':
                return self.leader[0]

    def register(self):
        self.ip_address = app.config['port']
        args = {'action':'register', 'address':self.ip_address}
        r = requests.get('http://127.0.0.1:8000/blockchain_platform', params=args)
        if r.status_code == 200:
            keys = json.loads(r.text)
            self.public_key[0] = keys['public_key']
            self.private_key[0] = keys['private_key']
            for neighbor in keys['neighbors']:
                self.neighbors.append(neighbor)
                neighbor = json.loads(neighbor)
                self.inform_neighbor(neighbor['address'])
            return r.text

    def mining(self):
        '''
        Mining a new block and broadcast it to all users 
        '''
        print('starting to mining')
        transactions = []
        q = Queue.PriorityQueue()
        s = set()
        while len(s) < 6:
            s.add(random.randint(0,len(self.tx_pool) - 1))
        for x in s:
            q.put(self.tx_pool[x])
        while(len(transactions) < 5):
            transactions.append(q.get())
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
            newblock = block(difficulty, time.time(), transactions, prev_hash, nonce)
            hash_val = newblock.calculate_hash()
            bin_hash_val = (bin(int(hash_val, 16))[2:] ).zfill(256)
        print(bin_hash_val)
        return newblock
        

    def transfer(self, new_tx):
        args = {'action':'gossip_transaction', 'transaction':new_tx}
        for neighbor in self.neighbors:
            print('neighbor')
            neighbor = json.loads(neighbor)
            print('neighbor address ' + str(neighbor['address']))
            url = 'http://127.0.0.1:' + str(neighbor['address']) + '/node'
            print('trying to gossip transaction ' + url)
            r = requests.get(url, params=args)
            print(r.text)
        return 'Making a transaction'

    def gossip_block(self, block):
        args = {'action':'gossip_block', 'block': block}
        for neighbor in self.neighbors:
            neighbor = json.loads(neighbor)
            url = 'http://127.0.0.1:' + str(neighbor['address']) + '/node'
            print('Trying to gossip block ' + url)
            r = requests.get(url, params=args)
        return 'Gossip a block'

    def announce_leader(self, address):
        args = {'action':'request_vote', 'leader': address}
        for neighbor in self.neighbors:
            neighbor = json.loads(neighbor)
            url = 'http://127.0.0.1:' + str(neighbor['address']) + '/node'
            print('Requesting vote from ' + str(neighbor['address']))
            r = requests.get(url, params=args)
        return 'Announcing leader, collecting votes'

    def vote(self, leader):
        balance = self.get_balance()
        if balance > 500:
            stake = round(random.uniform(0, 500), 2)
        else:
            stake = round(random.uniform(0, balance), 2)
        rand_block = json.loads(self.new_block_pool[random.randint(0,len(self.new_block_pool) - 1)])['block']
        block_hash = self.block_json_to_obj(rand_block).calculate_hash()
        v = vote(app.config['port'], block_hash, stake)
        args = {'action':'send_vote', 'vote': str(v)}
        url = 'http://127.0.0.1:' + leader + '/node'
        print('sending vote to leader ' + leader)
        r = requests.get(url, params=args)
        return

    def add_block(self, block):
        args = {'action':'add_block', 'block': block}
        for neighbor in self.neighbors:
            neighbor = json.loads(neighbor)
            url = 'http://127.0.0.1:' + str(neighbor['address']) + '/node'
            r = requests.get(url, params=args)
        return r.status_code

    def inform_neighbor(self, address):
        selfinfo = json.dumps({'address':app.config['port'],
                                'public_key':self.private_key[0]
                                })
        args = {'action':'add_neighbor', 'neighbor':selfinfo}
        url = 'http://127.0.0.1:' + address + '/node'
        r = requests.get(url, params=args)
        return r.text

    def get_balance(self):
        total_balance = 2000
        for block in self.blockchain:
            block = self.block_json_to_obj(block)
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
