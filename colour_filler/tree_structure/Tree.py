import itertools
import math
import re
from queue import SimpleQueue

from game_objects.Block import Move
from game_objects.game import Game
from tree_structure.Branch import Branch


class Tree:
    def __init__(self, block_locations, hole_locations, floor, size):
        hole_loc_combos = list(itertools.permutations(hole_locations, len(hole_locations)))
        self.puzzle_combinations = []
        for hc in hole_loc_combos:
            lst = []
            for i in range(len(hc)):
                lst.append((block_locations[i], hc[i]))
            self.puzzle_combinations.append(lst)
        self.roots = []
        self.starting_game_states = []
        for i in self.puzzle_combinations:
            for j in construct_game_state(floor, i, len(block_locations)):
                self.starting_game_states.append(j)
                branch = Branch(j)
                branch.data.box_to_space_ratio = len(block_locations) / size
                self.roots.append(branch)
        self.branches = {}
        self.floor_size = size
        for i in self.roots:
            self.branches[list(i.game_states)[0]] = i

    def evaluate(self):
        g = Game("1;1")
        for state in self.starting_game_states.copy():
            queue = SimpleQueue()
            branches = {state: self.branches[state]}
            seen_states = set()
            game_states = {}
            shortest_path = {}
            assert "Win" not in shortest_path.keys()
            queue.put(state)
            seen_states.add(state)
            game_states[state] = {Move.RIGHT: None, Move.LEFT: None, Move.UP: None, Move.DOWN: None}
            shortest_path[state] = {"prev": None, "length": 0, "dir_from_prev": None}
            while not queue.empty():
                current = queue.get()
                g.set_state(current)
                moves = game_states[current]
                for move in moves:
                    if moves[move] is None:
                        g.set_state(current)
                        new_state = g.movement(move)
                        moves[move] = new_state
                        if new_state not in seen_states:
                            seen_states.add(new_state)
                            shortest_path[new_state] = {"prev": current, "length": shortest_path[current]["length"] + 1, "dir_from_prev": move}
                            if not (new_state == "Lost" or new_state == "Win"):
                                queue.put(new_state)
                                game_states[new_state] = {Move.RIGHT: None, Move.LEFT: None, Move.UP: None, Move.DOWN: None}
                                if g.movement(Move.opposite(move)) == current:
                                    # add to branch
                                    branches[new_state] = branches[current]
                                    branches[current].add_state(new_state)
                                else:
                                    # new branch
                                    b = Branch(new_state, self.branches[state])
                                    cb = branches[current]
                                    b.reachable_from_branches.append(cb)
                                    branches[new_state] = b
                                    cb.branches.append(b)
                                    cb.data.branch_count += 1
                        elif shortest_path[new_state]["length"] > shortest_path[current]["length"] + 1:
                            shortest_path[new_state]["length"] = shortest_path[current]["length"] + 1
                            shortest_path[new_state]["prev"] = shortest_path[current]["prev"]
                            shortest_path[new_state]["dir_from_prev"] = move
                        if new_state == "Lost":
                            branches[current].data.dead_branches += 1
                        elif new_state == "Win":
                            branches[current].data.winning_branches += 1

            if "Win" in shortest_path.keys():
                branches[state].data.aggregated_game_states = len(set(branches.values()))
                branches[state].data.unique_game_states = len(branches.keys())
                branches[state].data.moves_to_win = str(shortest_path["Win"]["length"])
                branches[state].data.shortest_path = shortest_path
                self.branches.update(branches)
                prev = shortest_path["Win"]["prev"]
                moves = [shortest_path["Win"]["dir_from_prev"]]
                unique_tiles_index_set = set()
                while prev is not None:
                    split_state = re.split(r'[;|]', prev)
                    for i in range(len(split_state)):
                        s = split_state[i]
                        if "p" in s and "4" not in s:
                            unique_tiles_index_set.add(i)
                    moves.append(shortest_path[prev]["dir_from_prev"])
                    prev = shortest_path[prev]["prev"]
                game = Game(state)
                game.set_state(state)
                moves.reverse()
                for move in moves:
                    s = game.movement(move)
                    if s != "Win":
                        game.set_state(s)
                branches[state].data.unique_tiles_in_winning_path = len(unique_tiles_index_set)
                branches[state].data.map_percentage = len(unique_tiles_index_set)/self.floor_size
                branches[state].data.blocks_pushed = game.pushes

            else:
                self.roots.remove(self.branches[state])
                self.branches.pop(state)
                self.starting_game_states.remove(state)
        seen_branches = set()
        for branch in self.roots:
            DFS(branch, seen_branches)


def DFS(branch, seen_branches):
    if len(branch.branches) > 0:
        child_entropies = []
        for b in branch.branches:
            if b not in seen_branches:
                child_entropies.append(DFS(b, seen_branches))
        branch.data.global_entropy = calculate_local_entropy(branch.data.branch_count) + min(child_entropies)
        return branch.data.global_entropy
    if branch.data.winning_branches > 0:
        return branch.data.branch_count
    return 999

def calculate_local_entropy(count):
    return round(math.log2(count),2)


def shortest_path_player(root):
    state = root.game_states[0]
    game = Game(state)
    moves = []
    prev = root.data.shortest_path["Win"]["prev"]
    while prev is not state:
        print(prev)
        moves.append(root.data.shortest_path[prev]["dir_from_prev"])
        prev = root.data.shortest_path[prev]["prev"]
    for move in moves:
        print(game.movement(move))





"1;1;0|1;1a;0|1p;4a;4p"
def construct_game_state(floor, combinations, block_count):
    rows = floor.split("|")
    list_of_lists = []
    for row in rows:
        list_of_lists.append(row.split(";"))
    chars = "abcde"
    counter = 0
    for c1 in combinations:
        for c in c1:
            list_of_lists[c[0]][c[1]] = list_of_lists[c[0]][c[1]] + chars[counter]
        counter += 1
    state = ""
    for row in list_of_lists:
        for cell in row:
            state += str(cell) + ";"
        state = state[:-1]
        state += "|"
    state = state[:-1]
    state_list = []
    for i in range(block_count):
        state_list.append(state.replace(chars[i], "p"))
    return state_list
if __name__ == '__main__':
    # t = Tree([(1,1), (2,0)], [(2,1), (2,2)], "1;1;0|1;1;0|1;4;4")
    t = Tree([(1,3), (2,2), (2,3), (3,3)], [(0,3), (1,4), (2,4), (3,0)], "0;0;0;4;0|0;1;1;1;4|0;1;1;1;4|4;1;1;1;1|0;0;0;1;0", 15)
    t.MCTS()
    # print(construct_game_state("1;1;0|1;1;0|1;4;4", [((1,1), (2,1)), ((2,0), (2,2))]))
