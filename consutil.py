

class vote:
    def __init__(self, from_address, blockhash, stake ):
        self.from_address = from_address
        self.blockhash = blockhash
        self.stake = stake

class consutil
	def add_vote_pool(self,vote_info):
        """
        type: votes_info json str '{"voter":pk of voter,"blockhash":blockhash,"stake":staked money}'
        """
        if self.can_add_vote: 
            vote_json = json.loads(vote_info)
            new_vote = vote(vote_json["blockhash"],vote_json["stake"])
            self.vote_pool.append(new_vote)


    def vote_sum(self):
        """
        - If this node is selected as the leader, then it use this function to summarize the votes.
        - check stake money is valid for each voter
        - manage stake fee and transaction processing fee (give the processing fee to miner)
        """

        self.can_add_vote = False # lock the vote_pool 

        # check if each stake is valid, if not, discard the invalid votes
        valid_votes = []
        for voter in self.vote_pool:
            #voter_prob.append(voter.stake/total)
            voter_balance = self.get_balance(voter.from_address)
            if voter.stake <= voter_balance:
                valid_votes.append(voter)

        vote_blocks = {}
        for voter in valid_votes:
            if voter.blockhash in vote_blocks:
                vote_blocks[voter.blockhash] += voter.stake
            else:
                vote_blocks[voter.blockhash] = voter.stake

        sorted_voted_blocks = sorted(vote_blocks.items(), lambda x: x[1], reverse = True)
        final_block = sorted_voted_blocks[0] 
        # final_block = (blockhash, total stake for this block)
        # broadcast the final block to the net and let other node add this block to their chain

        # dispatching the processing fee to miner by making a transaction with the priority to be mined

        ## to be done here

        self.can_add_vote = True

        return final_block	