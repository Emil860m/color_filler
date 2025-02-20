from enum import Enum

from Block import Block, Move
from Cell import Tile
from Grid import Grid


class GameController(Enum):
    CONTINUE = 1
    LOST = 0
    WON = 2

class Game:
    def __init__(self, state=None, grid=None):
        if not state is None:
            self.grid = Grid(state=state)
        elif not grid is None:
            self.grid = Grid(tiles=grid)
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
        if self.grid.get_tile(self.player_block.x, self.player_block.y) == Tile.DISAPPEARING:
            self.grid.set_tile(self.player_block.x, self.player_block.y, str(Tile.EMPTY))
        else:
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

