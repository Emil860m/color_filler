import math

from game_objects.Block import Move
from game_objects.game import Game

moves = [Move.RIGHT, Move.LEFT, Move.UP, Move.DOWN]
class Branch:
    def __init__(self, state):
        self.states = {state}
        self.children = set()
        self.entropy = 0

    def get_entropy(self):
        if len(self.children) == 0:
            return 999.0
        return round(math.log2(len(self.children)), 1)

def evaluation(level):
    seen_states = set()
    seen_states.add(level)
    branch = level.replace("1p", "1")
    branches = {branch: Branch(level)}
    game_states = {level: {Move.RIGHT: None, Move.LEFT: None, Move.UP: None, Move.DOWN: None}}
    recursive_evaluation(level, seen_states, branches, game_states)
    return recursive_find_entropies(branch, branches, {branch})


def recursive_evaluation(current_level, seen_states, branches, game_states):
    game = Game(state="1;1|1;1")
    gs = game_states[current_level]
    old_branch = current_level.replace("1p", "1")
    for move in moves:
        game.set_state(current_level)
        new_state = game.movement(move)
        new_branch = new_state.replace("1p", "1")
        if new_branch in branches.keys():
            branches[new_branch].states.add(new_state)
            if current_level not in branches[new_branch].states:
                branches[old_branch].children.add(new_branch)
        else:
            branches[new_branch] = Branch(new_state)
            assert old_branch in branches.keys()
            branches[old_branch].children.add(new_branch)
        gs[move] = new_state
        if new_state not in seen_states:
            seen_states.add(new_state)
            if new_state != "Lost" and new_state != "Win":
                game_states[new_state] = {Move.RIGHT: None, Move.LEFT: None, Move.UP: None, Move.DOWN: None}
                recursive_evaluation(new_state, seen_states, branches, game_states)

def recursive_find_entropies(branch_name, branches, seen_branches):
    if branch_name == "Win":
        return 0
    if branch_name == "Lost":
        return 999
    branch = branches[branch_name]
    entropies = []
    for b in branch.children:
        if b not in seen_branches:
            seen_branches.add(b)
            entropies.append(recursive_find_entropies(b, branches, seen_branches))
    if len(entropies) == 0:
        return 999
    return branch.get_entropy() + min(entropies)
if __name__ == '__main__':
    level8 = "0;0;0;4p;0|0;1;1;1a;4a|0;1;1b;1c;4b|4c;1;1;1p;1|0;0;0;1;0"
    # level2 = "1;1;0|1;1a;0|1p;4a;4p"
    print(evaluation(level8))