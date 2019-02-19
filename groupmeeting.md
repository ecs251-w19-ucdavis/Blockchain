##404 NotFound Group Meeting

###What we have done:
We have built all classes, Node, Blockchain_Util, Block, and Transaction, and designed the structure of this blockchain and finished some of the functions. In the past week, Zhiyang was responsible for block design, Chuan did the node design, Yu achieved the transaction creation and management, Yue has finished some functions blockchain utilities module.  

###What we are going to details about our hybrid consensus next week, especially the voting part.
1.	Considering using merkle tree to hash all transactions hierarchically. Right now, we just concatenate all transaction information together to get a hash for the whole thing.
2.	Broadcast by gossip
3.	Ignore orphan transaction
4.	Traverse Blockchain to get the balance 
5.	Voting mechanism:
-	All members related to the transactions in new blocks which are waiting to be voted to enter the chain are potential voters. They will enter the voter pool and stake some money to be selected as an official voter. And the probability that they will be selected is related to the amount of the money they stake. 
-	New blocks generated in 5 seconds will be voted, and their final score will depend on the voters. If any blocks have the same final score, the earliest generated one will win. For example, 5 new blocks are generated at each second, A, B, C, D, E, after voting, scores for 5 blocks are, let’s say, 10, 10, 10.1, 10.1, 10.1.  Then block C will enter the chain. 
-	There also is a voting pool to collect all newly generated blocks to be voted. 

