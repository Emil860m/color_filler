import random

from remaster.Evaluation import evaluation


def genetic_algorithm(n_pop, n_iter, r_mut, size, box_count, special_tiles):
    pop = [generate_level(size, box_count, special_tiles) for _ in range(n_pop)]

    best, best_eval = pop[0], evaluate(pop[0])
    scores = [evaluate(c) for c in pop]
    for i in range(n_pop):
        if scores[i] > best_eval:
            best, best_eval = pop[i], scores[i]
            print(">%d, new best f(%s) = %.3f, length: %d" % (0, array_to_str(pop[i]), scores[i], len(get_floor_tiles(best, size))))
    for gen in range(1, n_iter):
        print("Iteration " + str(gen))
        selected = [selection(pop, scores) for _ in range(n_pop-1)]
        children = [best]
        for i in range(0, n_pop-1):
            c = str_to_array(array_to_str(selected[i]))
            mutation(c, r_mut, size)
            children.append(c)
        # replace population
        pop = children
        scores = [evaluate(c) for c in pop]

        for i in range(n_pop):
            if scores[i] > best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %.3f, length: %d" % (gen, array_to_str(pop[i]), scores[i], len(get_floor_tiles(best, size))))
    return [best, best_eval]


def validate(level) -> bool:
    return evaluate(level) >= 0


def str_to_array(level_str):
    return [[cell for cell in row.split(";")] for row in level_str.split("|")]


def array_to_str(level_array):
    level_str = ""
    for row in level_array:
        for cell in row:
            level_str += cell
            level_str += ";"
        level_str = level_str[:-1]
        level_str += "|"
    level_str = level_str[:-1]
    return level_str


def get_floor_tiles(level_array, size) -> []:
    tiles = []
    for i in range(size):
        for j in range(size):
            if not level_array[i][j] == "0":
                tiles.append((i, j))
    random.shuffle(tiles)
    return tiles


def generate_level(size, box_count, special_tiles) -> []:
    level = [["0" for _ in range(size)] for _ in range(size)]
    x, y = random.randrange(0, size), random.randrange(0, size)
    stck = [(x, y)]
    for _ in range(size * size):
        x, y = stck.pop()
        level[x][y] = "1"
        for i in range(-1, 2, 2):
            if size - 1 >= x + i >= 0:
                stck.append((x + i, y))
            if size - 1 >= y + i >= 0:
                stck.append((x, y + i))
        random.shuffle(stck)
    level_copy = array_to_str(level)
    validated = False
    while not validated:
        level = str_to_array(level_copy)
        floor_tiles = get_floor_tiles(level, size)
        for x, y in floor_tiles[:special_tiles]:
            level[x][y] = "2"
        letters = "pabcd"
        count = 0
        for x, y in floor_tiles[special_tiles:special_tiles + box_count]:
            level[x][y] = "4" + letters[count]
            count += 1
        count = 0
        for x, y in floor_tiles[special_tiles + box_count:special_tiles + box_count + box_count]:
            level[x][y] += letters[count]
            count += 1
        validated = validate(level)
    return level


def selection(pop, scores, k=3) -> []:
    # first random selection
    selection_ix = random.randrange(len(pop))
    for ix in range(random.randrange(0, len(pop), k - 1)):
        # check if better (e.g. perform a tournament)
        if scores[ix] > scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]


def mutation(level, r_mut, size):
    x, y = get_floor_tiles(level, size)[0]
    stck = [(x, y)]
    for _ in range(size * size * 2):
        x, y = stck.pop()
        if random.random() < r_mut:
            if level[x][y] == "1":
                level[x][y] = "0"
            elif level[x][y] == "0":
                level[x][y] = "1"
            elif "1" in level[x][y]:
                floor_tiles = get_floor_tiles(level, size)
                xi, yi = floor_tiles[0]
                level[x][y], level[xi][yi] = level[xi][yi], level[x][y]
            elif "4" in level[x][y]:
                floor_tiles = get_floor_tiles(level, size)
                xi, yi = floor_tiles[0]
                level[x][y], level[xi][yi] = level[xi][yi], level[x][y]
            elif level[x][y] == "2":
                floor_tiles = get_floor_tiles(level, size)
                xi, yi = floor_tiles[0]
                level[x][y], level[xi][yi] = level[xi][yi], level[x][y]
        for i in range(-1, 2, 2):
            if size - 1 >= x + i >= 0:
                stck.append((x + i, y))
            if size - 1 >= y + i >= 0:
                stck.append((x, y + i))
        random.shuffle(stck)


def evaluate(level) -> int:
    return evaluation(array_to_str(level))


if __name__ == "__main__":
    size = 5
    box_count = 4
    special_tiles = 2
    # define the total iterations
    n_iter = 20
    # define the population size
    n_pop = 20
    # mutation rate
    r_mut = 1.0 / float(size * 2)
    # n_pop, n_iter, r_cross, r_mut, size, box_count, special_tiles
    lst = genetic_algorithm(n_pop, n_iter, r_mut, size, box_count, special_tiles)
    print(array_to_str(lst[0]), lst[1])
