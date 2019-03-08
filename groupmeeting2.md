#### What we have done this week:
-	Build the [platform service](https://github.com/ecs251-w19-ucdavis/Blockchain/blob/master/Platform_Service.py) working as the user registration platform by user sending request through [console](https://github.com/ecs251-w19-ucdavis/Blockchain/blob/master/console.py).  
-	 Rebuild [node class, add mining, transfer, get balance, and broadcast information](https://github.com/ecs251-w19-ucdavis/Blockchain/blob/master/Node.py) by gossip functions in this class. Also decide to put all voting information and new generated information in node class.
-	Decide the form of gossip. For simulation, we will only try different ports in local, so the gossip will be realized by “get” request,
-	Redesign voting mechanism. Now everyone can vote in a period, after they vote, they will pass this information to neighbors, then every node collect the vote, once there are more than 1/3 of the whole network voting information in their voting pool, they begin be calculate the weight and decide which block should enter the chain, then he broadcast it to his neighbors until the whole network is covered. The block with most weight enters the chain after everyone finish their calculation.
-	In simulation, each node vote for earliest generated block that contains their transaction if they have made some transaction. Otherwise, they vote for the earliest generated block. 


#### What we are going to do next week:
-	Limit the number of transactions in one block, say, 10. Miner selects 15 transactions, and only pick 10 transactions with highest transaction service fee.
-	Finish all functions of the node class and voting mechanism. 
-	Try to run the simulation. We assign different money to each new nodes, and add double spending attack when make transaction, after the length of blockchain is greater than 100, we calculate the balance of each one to see if there are some nodes whose balance is illegal based on the information in the blockchain.

#### Trello
[https://trello.com/b/xvtDboDY/hybrid-consensus-for-blockchain](https://trello.com/b/xvtDboDY/hybrid-consensus-for-blockchain)
