from enum import Enum


class Move(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

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

    def get_value(self):
        return self.value

    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.value)