from console import *
import threading

def mining(i):
      portnum = 8001 + i
      print(str(portnum) + ' started mining')
      console(portnum).mine()
      return
 
if __name__ == "__main__":
      for i in range(3):
            t = threading.Thread(target=mining, args=(i,))
            t.start()