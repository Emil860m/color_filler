import heapq

from game_objects.Block import Move
from game_objects.game import Game

level2 = "1;1;0|1;1a;0|1p;4a;4p"
level8 = "0;0;0;4p;0|0;1;1;1a;4a|0;1;1b;1c;4b|4c;1;1;1p;1|0;0;0;1;0"
# level8 = "0;0;0;4c;0|0;1;1;1a;4a|0;1;1b;1c;4b|4p;1;1;1p;1|0;0;0;1;0"

level9 = "0;1;1;1;1|4a;1;1b;1a;4p|1;1;1;1c;1|4c;0;4b;1p;1"
# level = "0;0;0;0;0;4b;0;0;0|2;4c;0;0;0;1;2;4d;0|2;1;1;2;2;1a;1p;1c;0|4a;1;1;0;0;1;1d;1;1|0;0;1;2;2;1b;1;1;1|0;0;0;0;0;0;2;2;4p|0;0;0;0;0;0;0;0;0|0;0;0;0;0;0;0;0;0|0;0;0;0;0;0;0;0;0"
level = "1;1;1;0;0;0;0|1;0;1a;1;1;1;1|1;1b;1d;4a;4d;4b;4p|1;0;1;1p;0;0;0|1;1;1;0;0;0;0|0;0;0;0;0;0;0|0;0;0;0;0;0;0"

def solver(game_string):
    g = Game(state=game_string)
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
        print(state)
        for move in gs:
            if gs[move] is None:
                # g.set_state(state)
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
    print(seen_states)
    print(len(seen_states))
    print("Win" in seen_states)
    print("Win in " + str(shortest_path["Win"]["length"]) + " steps")
    prev = shortest_path["Win"]["prev"]
    while prev != game_string:
        print(prev)
        prev = shortest_path[prev]["prev"]
solver(level2)