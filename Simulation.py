from console import *
from Transaction import *
if __name__ == "__main__":
    # nodeone = node()
    # newblock = utils.create_genesis_block()
    # print(newblock)
    # nodeone.blockchain.append(newblock)
    # print(nodeone.blockchain)
    # start_time = time.time()
    # blocktwo = nodeone.mining([])
    # print("--- %s seconds ---" % (time.time() - start_time))
    # print(blocktwo)
    # print(blocktwo.calculate_hash())
    # console(8001).register()
    # console(8002).register()
    # console(8003).register()
    # console(8004).register()
    tx = transaction('1','1',10, '1')
    print(tx)
