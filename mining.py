from console import *
import threading

def mining(i):
      portnum = 8001 + i
      print(str(portnum) + ' started mining')
      console(portnum).mine()
      return
 
if __name__ == "__main__":
      threads = []
      for i in range(3):
            threads.append(threading.Thread(target=mining, args=(i,)))
      for t in threads:
            t.start()
      for t in threads:
            t.join()