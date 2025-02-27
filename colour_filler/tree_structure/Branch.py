from DataCollector import DataCollector



class Branch:
    def __init__(self, game_state):
        self.dead = False
        self.branches = [] # All branches reachable from this branch
        self.leaves = [] # All end states reachable from this branch


        self.game_states = [game_state] # All states contained in this branch
        # self.routes_between_states = [] # How to get to any other game state in the branch from all other

        # branch data
        self.data = DataCollector()

    def collect_data(self):
        for b in self.branches:
            self.data.merge_data(b.collect_data())
        return self.data

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