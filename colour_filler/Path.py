

class Path:
    def __init__(self, next, prev, move, game_state):
        self.next = next
        self.prev = prev
        self.move = move
        self.game_state = game_state

