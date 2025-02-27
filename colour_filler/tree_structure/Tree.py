import itertools

from tree_structure.Branch import Branch


class Tree:
    def __init__(self, block_locations, hole_locations, floor):
        hole_loc_combos = list(itertools.permutations(hole_locations, len(hole_locations)))
        self.puzzle_combinations = []
        for hc in hole_loc_combos:
            lst = []
            for i in range(len(hc)):
                lst.append((block_locations[i], hc[i]))
            self.puzzle_combinations.append(lst)
        self.roots = []
        for i in self.puzzle_combinations:
            for j in construct_game_state(floor, i, len(block_locations)):
                self.roots.append(Branch(j))
        # self.roots = [Branch(construct_game_state(floor, i, len(block_locations))) for i in self.puzzle_combinations]
        self.branches = {}
        for i in self.roots:
            # print(i.game_states)
            self.branches[list(i.game_states.keys())[0]] = i

    def MCTS(self):
        for branch in self.roots:
            branch.check_moves_from_states(self.branches)
        for i in self.roots:
            print(i.data.winning_branches)
        s = set(self.branches)
        print(s)
        print(len(self.branches))

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
t = Tree([(1,1), (2,0)], [(2,1), (2,2)], "1;1;0|1;1;0|1;4;4")
t.MCTS()
# print(construct_game_state("1;1;0|1;1;0|1;4;4", [((1,1), (2,1)), ((2,0), (2,2))]))
