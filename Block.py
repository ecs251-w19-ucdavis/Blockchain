#--------------------------------------------
# This 
#
#--------------------------------------------
class head:
    version = 0.1
    def __init__(self, data):
        self.data = data
        
    def versionUpdate(self, versionNum):
        self.version = versionNum
    
    def __str__(self):
        return "BlockChain Verion " + str(self.version)

# class body:
#     def

# class block:
