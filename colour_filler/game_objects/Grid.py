from game_objects.Cell import Cell


def create_tiles_from_string(s):
    rows = s.split("|")
    grid = [row.split(";") for row in rows]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = Cell(j, i, grid[i][j])
    return grid


class Grid:
    def __init__(self,  state=None, tiles=None):
        if not state is None:
            self.tiles = create_tiles_from_string(state)
        self.width = len(self.tiles[0])
        self.height = len(self.tiles)

    def print_grid(self):
        for row in self.tiles:
            for tile in row:
                print(tile, end=" ")
            print("")

    def get_tile(self, x, y):
        return self.tiles[y][x]

    def set_tile(self, x, y, tile):
        self.tiles[y][x] = tile
