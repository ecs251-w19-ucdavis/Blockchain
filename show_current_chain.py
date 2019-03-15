from consutil import *
import random
from console import *
import json
if __name__ == "__main__":
      blockchain = json.loads(console(8001).show_blockchain())
      for b in blockchain:
            block = json.loads(b)
            print json.dumps(block, indent = 2)