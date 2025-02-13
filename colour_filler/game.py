import heapq
import queue
from enum import Enum
from inspect import stack


class Tile(Enum):
    EMPTY = 0
    NORMAL = 1
    DISAPPEARING = 2
    PUSH = 3
    HOLE = 4
    GREY_HOLE = 5

class Move(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class Game_controller(Enum):
    CONTINUE = 1
    LOST = 0
    WON = 2




class Grid:
    def __init__(self,  state=None, tiles=None):
        if not state is None:
            self.tiles = create_from_string(state)
        self.width = len(self.tiles[0])
        self.height = len(self.tiles)

    def print_grid(self):
        for row in self.tiles:
            for tile in row:
                print(tile, end=" ")
            print("")

    def get_tile(self, x, y):
        return self.tiles[y][x]

    def set_tile(self, x, y, tile):
        self.tiles[y][x] = tile


def create_from_string(s):
    rows = s.split("|")
    grid = [row.split(";") for row in rows]
    return grid

class Block:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def move(self, move):
        if move == Move.UP:
            self.y -= 1
        elif move == Move.DOWN:
            self.y += 1
        elif move == Move.LEFT:
            self.x -= 1
        elif move == Move.RIGHT:
            self.x += 1

    def __str__(self):
        return str(self.x) + ", " + str(self.y)

class Game:
    def __init__(self, state=None, tiles=None):
        if not state is None:
            self.grid = Grid(state=state)
        elif not tiles is None:
            self.grid = Grid(tiles=tiles)
        else:
            print("State or tiles must be provided")
            exit(1)
        y = 0
        self.blocks = []
        self.blocks_to_move = []
        for row in self.grid.tiles:
            x = 0
            for tile in row:
                if len(tile) > 0:
                    if "p" in tile and "4" not in tile:
                        self.player_block = Block(x, y, "p")
                    elif len(tile) > 1 and "4" not in tile:
                        self.blocks.append(Block(x,y, tile[1]))
                x = x + 1
            y = y + 1

    def movement(self, move):
        if not self.valid_move(self.player_block.x, self.player_block.y, move):
            return self.get_state()
        for block in self.blocks_to_move:
            self.grid.set_tile(block.x, block.y, self.grid.get_tile(block.x, block.y)[:-1])
            block.move(move)
            self.grid.set_tile(block.x, block.y, self.grid.get_tile(block.x, block.y) + block.value)
            if "p" + block.value in self.grid.get_tile(block.x, block.y):
                return "Lost"
            if block.value * 2 in self.grid.get_tile(block.x, block.y):
                self.blocks.remove(block)
                self.grid.set_tile(block.x, block.y, "1")
            for b in self.blocks:
                if b.value in self.grid.get_tile(block.x, block.y) and not b.value == block.value:
                    return "Lost"
        self.blocks_to_move = []
        self.grid.set_tile(self.player_block.x, self.player_block.y, self.grid.get_tile(self.player_block.x, self.player_block.y)[:-1])
        self.player_block.move(move)
        self.grid.set_tile(self.player_block.x, self.player_block.y, self.grid.get_tile(self.player_block.x, self.player_block.y) + self.player_block.value)
        if "pp" in self.grid.get_tile(self.player_block.x, self.player_block.y):
            if len(self.blocks) > 0:
                return "Lost"
            return "Win"
        for b in self.blocks:
            if b.value in self.grid.get_tile(self.player_block.x, self.player_block.y) and not b.value == self.player_block.value:
                return "Lost"
        return self.get_state()


    def get_state(self):
        state = ""
        for row in self.grid.tiles:
            for cell in row:
                if len(cell) > 2:
                    print(cell)
                    exit(1)
                state += cell + ";"
            state = state[:-1]
            state += "|"
        state = state[:-1]
        if not "p" in state:
            print("not p")
        return state


    def valid_move(self, x, y, move):
        new_x = x
        new_y = y
        if move == Move.UP:
            new_y = y - 1
        elif move == Move.DOWN:
            new_y = y + 1
        elif move == Move.LEFT:
            new_x = x - 1
        elif move == Move.RIGHT:
            new_x = x + 1
        if (self.grid.height - 1 >= new_y >= 0) and (self.grid.width - 1 >= new_x >= 0):
            if self.grid.get_tile(new_x, new_y) == "0":
                return False
            for b in self.blocks:
                if b.x == new_x and b.y == new_y:
                    valid = self.valid_move(new_x, new_y, move)
                    if valid:
                        self.blocks_to_move.append(b)
                    return valid
            return True
        return False

    def set_state(self, state):
        if not state is None:
            self.grid = Grid(state=state)
        else:
            print("State or tiles must be provided")
            exit(1)
        y = 0
        self.blocks = []
        self.blocks_to_move = []
        for row in self.grid.tiles:
            x = 0
            for tile in row:
                if len(tile) > 0:
                    if "p" in tile and "4" not in tile:
                        self.player_block = Block(x, y, "p")
                    elif len(tile) > 1 and "4" not in tile:
                        self.blocks.append(Block(x,y, tile[1]))
                x = x + 1
            y = y + 1

s8 = "0;0;0;4p;0|0;1;1;1a;4a|0;1;1b;1c;4b|4c;1;1;1p;1|0;0;0;1;0"
s9 = "0;1;1;1;1|4a;1;1b;1a;4p|1;1;1;1c;1|4c;0;4b;1p;1"
s2 = "1;1;0|1;1a;0|1p;4a;4p"

g = Game(state=s9)

game_states = {g.get_state(): {Move.RIGHT: None, Move.LEFT: None, Move.UP: None, Move.DOWN: None}}
print(game_states)
shortest_path = {g.get_state(): {"prev": None, "length": 0}}
que = []
heapq.heappush(que, g.get_state())
seen_states = set()
seen_states.add(g.get_state())
while len(que) > 0:
    state = heapq.heappop(que)
    g.set_state(state)
    gs = game_states[state]
    for move in gs:
        if gs[move] is None:
            g.set_state(state)
            new_state = g.movement(move)
            gs[move] = new_state
            if new_state not in seen_states:
                seen_states.add(new_state)
                shortest_path[new_state] = {"prev": state, "length": shortest_path[state]["length"] + 1}
                if not (new_state == "Lost" or new_state == "Win"):
                    heapq.heappush(que, new_state)
                    game_states[new_state] = {Move.RIGHT: None, Move.LEFT: None, Move.UP: None, Move.DOWN: None}
            elif shortest_path[new_state]["length"] > shortest_path[state]["length"] + 1:
                shortest_path[new_state]["length"] = shortest_path[state]["length"] + 1
                shortest_path[new_state]["prev"] = shortest_path[state]["prev"]
print(len(seen_states))
print("Win" in seen_states)
prev = shortest_path["Win"]["prev"]
print("Win in " + str(shortest_path["Win"]["length"]) + " steps")
while prev != s9:
    print(prev)
    prev = shortest_path[prev]["prev"]
