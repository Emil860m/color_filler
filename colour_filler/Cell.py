from enum import Enum

from Block import Block

class Tile(Enum):
    EMPTY = 0
    NORMAL = 1
    DISAPPEARING = 2
    PUSH = 3
    HOLE = 4
    GREY_HOLE = 5

def get_tile_from_str(tile_str):
    if tile_str == Tile.EMPTY:
        return Tile.EMPTY
    elif tile_str == Tile.NORMAL:
        return Tile.NORMAL
    elif tile_str == Tile.DISAPPEARING:
        return Tile.DISAPPEARING
    elif tile_str == Tile.PUSH:
        return Tile.PUSH
    elif tile_str == Tile.HOLE:
        return Tile.HOLE
    elif tile_str == Tile.GREY_HOLE:
        return Tile.GREY_HOLE

class Cell:
    def __init__(self, x, y, tile):
        self.x = x
        self.y = y
        if len(tile) > 1:
            self.tile = get_tile_from_str(tile[0])
            self.block = Block(x,y, tile[1])
        else:
            self.tile = get_tile_from_str(tile)
            self.block = None
        self.block_counter = 0
        self.player_counter = 0

    def get_block(self):
        return self.block

    def set_block(self, block):
        self.block = block