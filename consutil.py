
import json
import math
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
    @staticmethod
    def vote_json_to_obj(vote_list):
        """
        type: list of json string
        rtype: list of vote object 
        """
        obj_list = []
        for voter in vote_list:
            vote_json = json.loads(voter)
            obj_list.append(vote(from_address = vote_json["from_address"], blockhash = vote_json["blockhash"], stake = vote_json["stake"]))
        return obj_list

    @staticmethod
    def vote_sum(raw_vote_list):
        zero_stake = False
        vote_obj_list = consutil.vote_json_to_obj(raw_vote_list)
        vote_list = []
        print("\n\n================================================")
        for voter in vote_obj_list:
            if voter.stake != 0:
                vote_list.append(voter)
            else:
                print(str(voter) + " " + "is in valid")
                zero_stake = True
        print("================================================\n\n")
        nums = len(vote_list)
        vote_list.sort(key = lambda x : x.stake, reverse = True)
        low, high = math.floor(nums*0.682), math.floor(nums*0.954) 
        for i in range(nums):
            if i <= low:
                vote_list[i].stake = 1
            elif i > low and i <= high:
                vote_list[i].stake = 2.5
            else:
                vote_list[i].stake = 14.8


        vote_blocks = {}
        for voter in vote_list:
            if voter.blockhash in vote_blocks:
                vote_blocks[voter.blockhash] += voter.stake
            else:
                vote_blocks[voter.blockhash] = voter.stake

        sorted_voted_blocks = sorted(vote_blocks.items(), key = lambda x: x[1], reverse = True)

        final_block_hash = sorted_voted_blocks[0][0] 

        return (final_block_hash, zero_stake)

# if __name__ == "__main__":
#     json_list = ['{"stake":0, "from_address": 8002, "blockhash": "1001a5c16393ac8a682c4150a142edc0807f67a58c2d46c4f77ae538ec417638"}',
#     '{"stake": 1000, "from_address": 8001, "blockhash": "2001a5c16393ac8a682c4150a142edc0807f67a58c2d46c4f77ae538ec417638"}',
#     '{"stake": 300, "from_address": 8003, "blockhash": "0001a5c16393ac8a682c4150a142edc0807f67a58c2d46c4f77ae538ec417638"}',
#     '{"stake": 0, "from_address": 8004, "blockhash": "0001a5c16393ac8a682c4150a142edc0807f67a58c2d46c4f77ae538ec417638"}',
#     '{"stake": 100, "from_address": 8001, "blockhash": "2001a5c16393ac8a682c4150a142edc0807f67a58c2d46c4f77ae538ec417638"}',
#     '{"stake": 300, "from_address": 8003, "blockhash": "0001a5c16393ac8a682c4150a142edc0807f67a58c2d46c4f77ae538ec417638"}',
#     '{"stake": 300, "from_address": 8004, "blockhash": "0001a5c16393ac8a682c4150a142edc0807f67a58c2d46c4f77ae538ec417638"}' ]
#     #print(json_list)
#     final_block_hash = consutil.vote_sum(json_list)
#     print(final_block_hash)


