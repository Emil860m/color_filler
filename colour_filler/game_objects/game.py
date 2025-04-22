from enum import Enum

from game_objects.Block import Block, Move
from game_objects.Cell import Tile
from game_objects.Grid import Grid


class GameController(Enum):
    CONTINUE = 1
    LOST = 0
    WON = 2

def check_level(level):
    valid = True
    if "1p" in level:
        if "4p" not in level:
            valid = False
    elif "4p" in level:
        valid = False

    if "1a" in level:
        if "4a" not in level:
            valid = False
    elif "4a" in level:
        valid = False

    if "1b" in level:
        if "4b" not in level:
            valid = False
    elif "4b" in level:
        valid = False

    if "1c" in level:
        if "4c" not in level:
            valid = False
    elif "4c" in level:
        valid = False

    if "1d" in level:
        if "4d" not in level:
            valid = False
    elif "4d" in level:
        valid = False
    return valid
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
        self.grey_blocks = []
        self.blocks_to_move = []
        for row in self.grid.tiles:
            x = 0
            for tile in row:
                if tile.block is not None:
                    if tile.block.value == "p":
                        self.player_block = Block(x, y, "p")
                    elif tile.block.value == "g":
                        self.grey_blocks.append(Block(x, y, "g"))
                    else:
                        self.blocks.append(Block(x,y, tile.block.value))
                x = x + 1
            y = y + 1

    def movement(self, move):
        if not self.valid_move(self.player_block.x, self.player_block.y, move):
            return self.get_state()
        for block in self.blocks_to_move:
            block.move(move, self.grid)
            if self.grid.get_tile(block.x, block.y).tile == Tile.HOLE:
                if not block.value == self.grid.get_tile(block.x, block.y).value:
                    return "Lost"
                else:
                    self.blocks.remove(block)
                    self.grid.set_tile(block.x, block.y, "1")
        self.blocks_to_move = []
        if self.grid.get_tile(self.player_block.x, self.player_block.y).tile == Tile.DISAPPEARING:
            self.grid.get_tile(self.player_block.x, self.player_block.y).tile = Tile.EMPTY
        self.player_block.move(move, self.grid)
        if self.grid.get_tile(self.player_block.x, self.player_block.y).tile == Tile.HOLE:
            if not self.player_block.value == self.grid.get_tile(self.player_block.x, self.player_block.y).value:
                return "Lost"
            else:
                if len(self.blocks) == 0:
                    return "Win"
                return "Lost"
        if self.grid.get_tile(self.player_block.x, self.player_block.y).tile == Tile.PUSH:
            #TODO: push tile logic
            pass
        for block in self.blocks:
            if self.grid.get_tile(block.x, block.y).tile == Tile.PUSH:
                #TODO: push tile logic
                pass
        return self.get_state()


    def get_state(self):
        state = ""
        for row in self.grid.tiles:
            for cell in row:
                state += str(cell) + ";"
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
            if self.grid.get_tile(new_x, new_y).tile == Tile.EMPTY:
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
            # if not check_level(state):
            #     print("ERROR", state)
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
                if tile.block is not None:
                    if tile.block.value == "p":
                        self.player_block = Block(x, y, "p")
                    else:
                        self.blocks.append(Block(x,y, tile.block.value))
                x = x + 1
            y = y + 1

