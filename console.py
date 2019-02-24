import requests
class console:
    def __init__(self, address):
        self.address = address

    def register(self):
        url = 'http://127.0.0.1:' + str(self.address) + '/node'
        args = {'action':'register'}
        r = requests.get(url, params=args)
        if r.status_code == 200:
            print(r.text)
            print('node 8001 is registered')
            return r.text