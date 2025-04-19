from enum import Enum

from game_objects.Block import Block, Move
from game_objects.Cell import Tile
from game_objects.Grid import Grid


class GameController(Enum):
    CONTINUE = 1
    LOST = 0
    WON = 2

class Game:
    def __init__(self, state=None, grid=None):
        self.pushes = 0
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
            self.pushes += 1
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
        tile = self.grid.get_tile(self.player_block.x, self.player_block.y).tile
        if tile == Tile.PUSH_RIGHT and self.valid_move(self.player_block.x, self.player_block.y, Move.RIGHT):
            self.player_block.move(Move.RIGHT, self.grid)
        if tile == Tile.PUSH_UP and self.valid_move(self.player_block.x, self.player_block.y, Move.UP):
            self.player_block.move(Move.UP, self.grid)
        if tile == Tile.PUSH_LEFT and self.valid_move(self.player_block.x, self.player_block.y, Move.LEFT):
            self.player_block.move(Move.LEFT, self.grid)
        if tile == Tile.PUSH_DOWN and self.valid_move(self.player_block.x, self.player_block.y, Move.DOWN):
            self.player_block.move(Move.DOWN, self.grid)
        if self.grid.get_tile(self.player_block.x, self.player_block.y).tile == Tile.HOLE:
            if not self.player_block.value == self.grid.get_tile(self.player_block.x, self.player_block.y).value:
                return "Lost"
            else:
                if len(self.blocks) == 0:
                    return "Win"
                return "Lost"

        for block in self.blocks:
            tile = self.grid.get_tile(block.x, block.y).tile
            if tile == Tile.PUSH_RIGHT and self.valid_move(block.x, block.y, Move.RIGHT):
                block.move(Move.RIGHT, self.grid)
            if tile == Tile.PUSH_LEFT and self.valid_move(block.x, block.y, Move.LEFT):
                block.move(Move.LEFT, self.grid)
            if tile == Tile.PUSH_UP and self.valid_move(block.x, block.y, Move.UP):
                block.move(Move.UP, self.grid)
            if tile == Tile.PUSH_DOWN and self.valid_move(block.x, block.y, Move.DOWN):
                block.move(Move.DOWN, self.grid)
            if self.grid.get_tile(block.x, block.y).tile == Tile.HOLE:
                if not block.value == self.grid.get_tile(block.x, block.y).value:
                    return "Lost"
                else:
                    self.blocks.remove(block)
                    self.grid.set_tile(block.x, block.y, "1")
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
            tile = self.grid.get_tile(new_x, new_y).tile
            if tile == Tile.EMPTY:
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
        if state == "Lost" or state == "Win":
            print("state is Lost or win:", state)
            assert not (state == "Lost" or state == "Win")
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
                if tile.block is not None:
                    if tile.block.value == "p":
                        self.player_block = Block(x, y, "p")
                    else:
                        self.blocks.append(Block(x,y, tile.block.value))
                x = x + 1
            y = y + 1

