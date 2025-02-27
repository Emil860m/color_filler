from tree_structure.Branch import Branch


class Tree:
    def __init__(self, block_locations, hole_locations):
        self.puzzle_combinations = [(b,h) for b in block_locations for h in hole_locations] # list of all possible combinations of blocks and holes
        self.puzzles = [Branch(i) for i in self.puzzle_combinations]

    def MCTS(self):
        pass

