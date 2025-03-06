from enum import Enum


class Move(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    @staticmethod
    def opposite(move):
        if move == Move.LEFT:
            return Move.RIGHT
        if move == Move.UP:
            return Move.DOWN
        if move == Move.RIGHT:
            return Move.LEFT
        if move == Move.DOWN:
            return Move.UP
        print("Invalid move")
        exit(1)


class Block:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def move(self, move, grid):
        grid.get_tile(self.x, self.y).block = None
        if move == Move.UP:
            self.y -= 1
        elif move == Move.DOWN:
            self.y += 1
        elif move == Move.LEFT:
            self.x -= 1
        elif move == Move.RIGHT:
            self.x += 1
        grid.get_tile(self.x, self.y).block = self

    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.value)