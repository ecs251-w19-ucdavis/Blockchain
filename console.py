import requests
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
    def transfer(self, destination, amount):
        args = {'action':'transfer', 'to_address':destination, 'amount': amount}
        r = requests.get(self.url, params=args)
        if r.status_code == 200:
            print('node ' + self.address + 'made a $' + str(amount) + ' transfer to ' + destination)
            return r.text
    
    # def 