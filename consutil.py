
import json
class vote:
    def __init__(self, from_address, blockhash, stake ):
        self.from_address = from_address
        self.blockhash = blockhash
        self.stake = stake

    def __str__(self):
        vote_str = json.dumps(self, default=lambda o: o.__dict__)
        # print(test_str)
        return vote_str

class consutil:
    def add_vote_pool(self,vote_info):
        if self.can_add_vote: 
            vote_json = json.loads(vote_info)
            new_vote = vote(vote_json["blockhash"],vote_json["stake"])
            self.vote_pool.append(new_vote)


    def vote_sum(self):
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
        self.can_add_vote = True

        return final_block	