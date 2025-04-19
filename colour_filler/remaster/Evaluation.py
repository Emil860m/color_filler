import math

from game_objects.Block import Move
from game_objects.game import Game

moves = [Move.RIGHT, Move.LEFT, Move.UP, Move.DOWN]


class Branch:
    def __init__(self, state):
        self.states = {state}
        self.children = list()
        self.child_entropies = {}
        self.entropy = 0

    def add_child(self, child):
        if child not in self.children and not child == "Lost":
            self.children.append(child)

    def get_entropy(self):
        if len(self.children) == 0:
            return 999.0
        # if "Lost" in self.children and len(self.children) > 1:
        #     return round(math.log2(len(self.children) - 1), 1)
        return round(math.log2(len(self.children)), 1)


def evaluation(level):
    seen_states = set()
    seen_states.add(level)
    branch = level.replace("1p", "1")
    branches = {branch: Branch(level)}
    game_states = {level: {Move.RIGHT: None, Move.LEFT: None, Move.UP: None, Move.DOWN: None}}
    shortest_path = {level: {"prev": None, "length": 0}}
    recursive_evaluation(level, seen_states, branches, game_states, shortest_path)
    entropy = recursive_find_entropies(branch, branches, {branch}, {})
    # if "Win" in shortest_path.keys():
    #     prev = shortest_path["Win"]["prev"]
    #     while prev != None:
    #         print(prev)
    #         prev = shortest_path[prev]["prev"]
    #     if "Win" in seen_states:
    #         print(len(seen_states))
    #         print("win found")
    if entropy > 998:
        return -1
    return entropy


def recursive_evaluation(current_level, seen_states, branches, game_states, shortest_path):
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
                branches[old_branch].add_child(new_branch)
        else:
            branches[new_branch] = Branch(new_state)
            assert old_branch in branches.keys()
            branches[old_branch].add_child(new_branch)
        gs[move] = new_state
        if new_state not in seen_states:
            shortest_path[new_state] = {"prev": current_level, "length": shortest_path[current_level]["length"] + 1}
            seen_states.add(new_state)
            if new_state != "Lost" and new_state != "Win":
                game_states[new_state] = {Move.RIGHT: None, Move.LEFT: None, Move.UP: None, Move.DOWN: None}
                recursive_evaluation(new_state, seen_states, branches, game_states, shortest_path)
        elif shortest_path[new_state]["length"] > shortest_path[current_level]["length"] + 1:
            shortest_path[new_state]["length"] = shortest_path[current_level]["length"] + 1
            shortest_path[new_state]["prev"] = shortest_path[current_level]["prev"]


def recursive_find_entropies(branch_name, branches, seen_branches, branch_entropies):
    if branch_name == "Win":
        return 0
    if branch_name == "Lost":
        return 999
    branch = branches[branch_name]
    entropies = []
    for b in branch.children:
        if b not in seen_branches:
            seen_branches.add(b)
            entropies.append(recursive_find_entropies(b, branches, seen_branches, branch_entropies))
        elif b in branch_entropies.keys():
            entropies.append(branch_entropies[b])
    if len(entropies) == 0:
        return 999
    branch_entropies[branch_name] = branch.get_entropy() + min(entropies)
    return branch.get_entropy() + min(entropies)


if __name__ == '__main__':
    level8 = "0;0;1;1;0|0;4p;1;1;0|2;1b;1;1;0|1;1a;1c;4c;4a|1p;1;1;2;4b"
    # level2 = "1;1;0|1;1a;0|1p;4a;4p"
    print(evaluation(level8))
