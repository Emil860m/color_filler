from DataCollector import DataCollector
from game_objects.Block import Move
from game_objects.game import Game


class Branch:
    def __init__(self, game_state):
        self.dead = False
        self.branches = [] # All branches reachable from this branch
        self.leaves = [] # All end states reachable from this branch


        self.game_states = {game_state: {Move.RIGHT: None, Move.LEFT: None, Move.UP: None, Move.DOWN: None}} # All states contained in this branch
        # self.routes_between_states = [] # How to get to any other game state in the branch from all other

        # branch data
        self.data = DataCollector()

    def collect_data(self):
        for b in self.branches:
            self.data.merge_data(b.collect_data())
        return self.data

    def check_moves_from_states(self, branches):
        game = Game("1;1|1;1")
        # print(self.game_states)
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
                        if not new_state == "Lost" and not new_state == "Win":
                            b.check_moves_from_states(branches)
                        if new_state == "Lost":
                            lost_found = True
                        if new_state == "Win":
                            win_found = True
                    elif new_state not in self.branches:
                        self.branches.append(branches[new_state])
        if lost_found:
            self.data.dead_branches += 1
        if win_found:
            self.data.winning_branches += 1
        for b in self.branches:
            self.data.merge_data(b.data)








    def create_leaf(self):
        pass

    def merge_branch(self, branch):
        # TODO: figure out how to take all references to the other branch to this one
        self.branches.append(branch.branches)
        self.leaves.append(branch.leaves)
        self.game_states.append(branch.game_states)
        self.data.merge_data(branch.data)

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