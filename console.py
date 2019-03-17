import requests
import time
import json
class console:
    def __init__(self, address):
        self.address = address
        self.url = 'http://127.0.0.1:' + str(self.address) + '/node'

    def register(self):
        args = {'action':'register'}
        r = requests.get(self.url, params=args)
        if r.status_code == 200:
            # print(r.text)
            print('node ' + str(self.address) + ' is registered')
            return r.text
        else:
            print('Failed to register ' + str(self.address))
            return

    def transfer(self, to_address, amount, fee):
        args = {'action':'transfer', 'to_address':to_address, 'amount': amount, 'fee': fee}
        r = requests.get(self.url, params=args)
        if r.status_code == 200:
            print('node ' + str(self.address) + ' made a $' + str(amount) + ' transfer to ' + to_address + ' with fee: ' + str(fee))
            return r.text
    
    def mine(self):
        args = {'action':'start_mining'}
        r = requests.get(self.url, params=args)
        if r.status_code == 200:
            print json.dumps(json.loads(r.text), indent =2)
            return r.text
        else:
            print('node ' + str(self.address) + ' failed to mine a block')
            return r.text

    def show_balance(self):
        args = {'action':'show_balance'}
        r = requests.get(self.url, params=args)
        if r.status_code == 200:
            print('node: ' + str(self.address) + ', balance: ' + str(r.text))

    def show_transactions(self):
        args = {'action':'show_transactions'}
        r = requests.get(self.url, params=args)
        if r.status_code == 200:
            print json.dumps(json.loads(r.text), indent =2)

    def show_blockchain(self):
        address_list = console.get_registered_users()
        url = 'http://127.0.0.1:' + str(self.address) + '/node'
        args = {'action':'show_blockchain'}
        r = requests.get(url, params=args)
        if r.status_code == 200:
            print json.dumps(json.loads(r.text), indent = 2)
            return r.text

    @staticmethod
    def get_registered_users():
        args = {'action':'get_registered_users'}
        r = requests.get('http://127.0.0.1:8000/blockchain_platform', params=args)
        user_list = json.loads(r.text)
        address_list = []
        for u in user_list:
            address = json.loads(u)['address']
            address_list.append(address)
            # print address
        return address_list

    @staticmethod
    def elect_block():
        address_list = console.get_registered_users()
        for address in address_list:
            url = 'http://127.0.0.1:' + str(address) + '/node'
            # print url
            args = {'action':'elect_block'}
            r = requests.get(url, params=args)
            if r.status_code == 200:
                if json.loads(r.text)['leader']:
                    print(r.text)
                # return r.text
    
   
    