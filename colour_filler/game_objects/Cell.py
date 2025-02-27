from enum import Enum

from game_objects.Block import Block

class Tile(Enum):
    EMPTY = 0
    NORMAL = 1
    DISAPPEARING = 2
    PUSH = 3
    HOLE = 4
    GREY_HOLE = 5

    @staticmethod
    def get_str_value_from_tile(value):
        if value == Tile.EMPTY:
            return "0"
        elif value == Tile.NORMAL:
            return "1"
        elif value == Tile.DISAPPEARING:
            return "2"
        elif value == Tile.PUSH:
            return "3"
        elif value == Tile.HOLE:
            return "4"
        elif value == Tile.GREY_HOLE:
            return "5"
        print("ERROR" + value)
        return "ERROR"

def get_tile_from_str(tile_str):
    if tile_str == "0":
        return Tile.EMPTY
    elif tile_str == "1":
        return Tile.NORMAL
    elif tile_str == "2":
        return Tile.DISAPPEARING
    elif tile_str == "3":
        return Tile.PUSH
    elif tile_str == "4":
        return Tile.HOLE
    elif tile_str == "5":
        return Tile.GREY_HOLE

class Cell:
    def __init__(self, x, y, tile):
        self.x = x
        self.y = y
        self.value = None
        if len(tile) > 1:
            self.tile = get_tile_from_str(tile[0])
            if not self.tile == Tile.HOLE:
                self.block = Block(x,y, tile[1])
            else:
                self.value = tile[1]
                self.block = None
        else:
            self.tile = get_tile_from_str(tile)
            self.block = None
        assert self.tile is not None
        self.block_counter = 0
        self.player_counter = 0

    def __str__(self):
        if self.block is not None:
            return str(Tile.get_str_value_from_tile(self.tile)) + str(self.block.value)
        if self.value is not None:
            return str(Tile.get_str_value_from_tile(self.tile)) + str(self.value)
        return Tile.get_str_value_from_tile(self.tile)

    def get_block(self):
        return self.block

    def set_block(self, block):
        self.block = block