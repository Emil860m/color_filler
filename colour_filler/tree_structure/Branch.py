from DataCollector import DataCollector
from game_objects.Block import Move
from game_objects.game import Game


class Branch:
    def __init__(self, game_state, start_branch=None):
        self.dead = False
        self.branches = [] # All branches reachable from this branch
        self.reachable_from_branches = []
        self.start_branch = start_branch
        # self.leaves = [] # All end states reachable from this branch


        self.game_states = [game_state] #TODO: should be line below
        # self.game_states = {game_state: {Move.RIGHT: None, Move.LEFT: None, Move.UP: None, Move.DOWN: None}} # All states contained in this branch
        # self.routes_between_states = [] # How to get to any other game state in the branch from all other

        # branch data
        self.data = DataCollector()

    def collect_data(self):
        for b in self.branches:
            self.data.merge_data(b.collect_data())
        return self.data

    def check_moves_from_states(self, branches):
        game = Game("1;1|1;1")
        print("doing", self.game_states)
        lost_found = False
        win_found = False
        for gs in self.game_states:
            for key in self.game_states[gs]:
                game.set_state(gs)
                if self.game_states[gs][key] is None:
                    new_state = game.movement(key)
                    self.game_states[gs][key] = new_state
                    if new_state not in branches.keys():
                        b = Branch(new_state)
                        branches[new_state] = b
                        # print(key, new_state)
                        if not new_state == "Lost" and not new_state == "Win":
                            b.check_moves_from_states(branches)
                        if new_state == "Lost":
                            lost_found = True
                        if new_state == "Win":
                            win_found = True
                        self.branches.append(b)
                    elif new_state not in self.branches and new_state not in self.game_states.keys():
                        self.branches.append(branches[new_state])
        print("done", self.game_states)
        for b in self.branches:
            if self in b.branches:
                print("merging", b.branches)
                self.merge_branch(b, branches)
        for b in self.branches:
            if b not in branches.values():
                print("Error")
        print("merged")

        # if lost_found:
        #     self.data.dead_branches += 1
        # if win_found:
        #     self.data.winning_branches += 1
        # # print("length: " + str(len(self.branches)))append
        # for b in self.branches:
        #     # print(b.data.winning_branches)
        #     if b is not self:
        #         self.data.merge_data(b.data)
        # if self.data.winning_branches > 0:
        #     print(self.game_states, self.data.winning_branches)
        # # if self.data.dead_branches > 0:
        # #     print(self.game_states)








    def create_leaf(self):
        pass

    def merge_branch(self, branch, branches):
        pass
        # TODO: figure out how to take all references to the other branch to this one
        # self.branches.extend(branch.branches)
        # self.branches.remove(self)
        # branch.branches = []
        # self.leaves.extend(branch.leaves)
        # self.game_states.update(branch.game_states)
        # self.data.merge_data(branch.data)
        # for gs in self.game_states:
        #     branches[gs] = self

    def add_child_branch(self, branch):
        self.branches.append(branch)
        self.data.merge_data(branch.data)

    def kill_branch(self):
        self.dead = True
        self.branches = []
        self.leaves = []

    def down_search(self, search):
        target_found = False
        for i in self.branches:
            target_found = i.downn_search(search)
        return target_found

    def add_state(self, state):
        self.game_states.append(state)

# br = Branch("1;1;0|1;1a;0|1p;4a;4p")
# brdict = {"1;1;0|1;1a;0|1p;4a;4p": br}
# br.check_moves_from_states(brdict)
# print(br.branches, "\n\n")
# print(len(set(brdict.values())))
