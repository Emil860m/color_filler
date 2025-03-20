from Path import Path


class DataCollector:
    def __init__(self):
        # unique game states data
        self.unique_game_states = 0
        self.game_states_set = set()
        self.box_to_space_ratio = 0


        # Winning path data
        # self.winning_path = Path()
        self.moves_to_win = 0
        self.map_percentage = 0
        self.unique_tiles_in_winning_path = 0
        self.shortest_path = {}
        self.blocks_pushed = 0


        # aggregated game states data
        self.aggregated_game_states = 0
        self.dead_branches = 0
        self.winning_branches = 0
        self.local_entropy = 0
        self.global_entropy = 0

    def merge_data(self, data):
        # should aggregate data from given object
        self.winning_branches += data.winning_branches
        self.dead_branches += data.dead_branches

    def calculate_value(self):
        pass


def calculate_data_values(data_objects):
    return [(d, d.calculate_value()) for d in data_objects]
