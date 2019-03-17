# !/usr/bin/python
from console import *
from Transaction import *
import Queue
import threading
def mining(i):
      portnum = 8001 + i
      print(str(portnum) + ' started mining')
      console(portnum).mine()
      return
 
if __name__ == "__main__":
    console(8001).register()
    console(8002).register()
    console(8003).register()
    console(8004).register()
    console(8005).register()
    console(8006).register()
    console(8001).show_balance()
    console(8002).show_balance()
    console(8002).transfer('8001', 600, 20)
    # console(8002).transfer('8001', 300, 20)
    console(8002).transfer('8003', 300, 22)
    # console(8001).transfer('8002', 400, 21)
    console(8002).transfer('8004', 800, 13)
    # console(8003).transfer('8002', 430, 14)
    # console(8004).transfer('8002', 430, 1)
    threads = []
    for i in range(3):
        threads.append(threading.Thread(target=mining, args=(i,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    console.elect_block()
    print("Showing blockchian")
    console(8001).show_blockchain()
    print("Showing transactions after a new block is added to the chain")
    console(8001).show_transactions()