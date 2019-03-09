import requests
import time
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
            print('node ' + str(self.address) + ' made a $' + str(amount) + ' transfer to ' + to_address)
            return r.text