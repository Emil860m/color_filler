# genetic algorithm
import random
from time import sleep

from numpy.random import randint, rand

from tree_structure.Tree import Tree


floor_generation_chance = 0.90


def genetic_algorithm(objective, n_bits, n_iter, n_pop, r_cross, r_mut, size, box_count, special_tiles):
    # number of boxes, disappearing tiles, push tiles, level size (floor spaces)
    # initial population of random bitstring
    # size * size array
    # pop = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]
    pop = []
    scores = []
    while len(pop) < 0.75 * n_pop:
        start = len(pop)
        pop.extend([generate(size, box_count, special_tiles) for _ in range(start, n_pop)])
        scores.extend([objective(pop[i][0], pop[i][1], pop[i][2], size) for i in range(start, len(pop))])
        temp = []
        temp_scores = []
        for i in range(n_pop):
            if (not scores[i] == -1) and (not scores[i] > 999):
                temp.append(pop[i])
                temp_scores.append(scores[i])
        pop = temp
        scores = temp_scores
    # keep track of best solution
    best, best_eval = pop[0], objective(pop[0][0], pop[0][1], pop[0][2], size)
    print(best, best_eval)
    # enumerate generations
    for gen in range(n_iter):
        print("----new iter " + str(gen) + "----")
        if not gen == 0:
            # evaluate all candidates in the population
            scores = [objective(c[0], c[1], c[2], size) for c in pop]
            # check for new best solution
        print("Trying to find new best")
        for i in range(len(scores)):
            if scores[i] > best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %.3f" % (gen, pop[i], scores[i]))
        temp = [best]
        for i in range(len(scores)):
            if (not scores[i] == -1) and (not scores[i] > 999):
                temp.append(pop[i])
        pop = temp
        print(pop)
        # select parents
        assert len(pop) > 0
        selected = [selection(pop, scores) for _ in range(n_pop)]
        # print(selected[0])
        # print("selected length:", len(selected))
        # create the next generation
        children = list()
        for i in range(0, n_pop - 1, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i + 1]
            # print(p1)
            # print(p2)
            # crossover and mutation
            for c in crossover(p1, p2, r_cross, box_count):
                # mutation
                # level, r_mut, size, box_array, box_count, hole_array, hole_count
                r = mutation(c[0], r_mut, size, c[3], box_count, c[2], box_count)
                # store for next generation
                children.append(r)
        # replace population
        # selected.extend(children)
        pop = children
        pop.append(best)
    return [best, best_eval]

def generate(size, box_count, special_tiles):
    generated = [[0 for i in range(size)] for j in range(size)]
    x, y = int(randint(size)/2), int(randint(size)/2)
    generated[x][y] = 1
    flipped = 0
    stack = [(x,y)]
    while True:
        (x, y) = stack.pop()
        for i in range(-1, 2, 2):
            if size-1 > x > 0 and generated[x + i][y] == 0 and random.uniform(0, 1) < floor_generation_chance:
                generated[x + i][y] = 1
                flipped += 1
            if size-1 > y > 0 and generated[x][y + i] == 0 and random.uniform(0, 1) < floor_generation_chance:
                generated[x][y + i] = 1
                flipped += 1
            if size-1 > x+i >= 0:
                stack.append((x + i, y))
            if size-1 > y+i >= 0:
                stack.append((x, y + i))
            random.shuffle(stack)
        if flipped > 0.5 * size*size:
            if validate(generated, size):
                break
    floor_tiles = []
    for i in range(size):
        for j in range(size):
            if generated[i][j] == 1:
                floor_tiles.append((i, j))
    random.shuffle(floor_tiles)
    for i in range(box_count):
        generated[floor_tiles[i][0]][floor_tiles[i][1]] = 4
    for i in range(box_count, box_count + special_tiles):
        # if random.uniform(0, 1) > 0.5:
        generated[floor_tiles[i][0]][floor_tiles[i][1]] = 2
        # else:
        #     push_tiles = "5678"
        #     generated[floor_tiles[i][0]][floor_tiles[i][1]] = random.choice(push_tiles)
    hole_locations = floor_tiles[:box_count]
    box_locations = floor_tiles[box_count + special_tiles:box_count + box_count + special_tiles]
    return generated, hole_locations, box_locations

def validate(level, size):
    list_of_coords = []
    for i in range(size):
        for j in range(size):
            if int(level[i][j]) > 0:
                if len(list_of_coords) == 0:
                    list_of_coords.extend(DFS(level, (i,j), size))
                elif (i,j) not in list_of_coords:
                    print("Not validated")
                    return False
    return True

def DFS(level, coords, size):
    ret_list = [coords]
    stack = []
    seen_coords = set()
    stack.append(coords)
    seen_coords.add(coords)
    while len(stack) > 0:
        coord = stack.pop()
        for i in range(-1, 2, 2):
            x, y = coord
            xi, yi = coord[0] + i, coord[1] + i
            if size > xi >= 0 and (xi, y) not in seen_coords:
                if level[xi][y] == 1:
                    seen_coords.add((xi, y))
                    stack.append((xi, y))
                    ret_list.append((xi, y))
            if size > yi >= 0 and (x, yi) not in seen_coords:
                if level[x][yi] == 1:
                    seen_coords.add((x, yi))
                    stack.append((x, yi))
                    ret_list.append((x, yi))
    return ret_list

# tournament selection
def selection(pop, scores, k=3):
    # first random selection
    if len(pop) == 1:
        return pop[0]
    selection_ix = randint(len(pop) - 1)
    for ix in randint(0, len(pop) - 1, k - 1):
        # check if better (e.g. perform a tournament)
        if scores[ix] > scores[selection_ix]:
            # print(scores[selection_ix])
            selection_ix = ix
    return pop[selection_ix]


# crossover two parents to create two children
def crossover(p1, p2, r_cross, box_count):
    size = len(p1)
    if p1 == p2:
        return [(p1[0], box_count, p1[1], p1[2])]
    # children are copies of parents by default
    not_validated = True
    while not_validated:
        c1, c2 = p1[0].copy(), p2[0].copy()
        # check for recombination
        if rand() < r_cross:
            # select crossover point that is not on the end of the string
            pt = randint(1, len(p1[0]) - 2)
            # perform crossover
            c1 = p1[0][:pt] + p2[0][pt:]
            c2 = p2[0][:pt] + p1[0][pt:]
        not_validated = validate(c1, size) and validate(c2, size)
    cell_count = 0
    for row in c1:
        for cell in row:
            if cell == 4:
                cell_count += 1
    return [(c1, cell_count, p1[1], p1[2]), (c2, (box_count*2) - cell_count, p2[1], p2[2])]


# mutation operator
def mutation(level, r_mut, size, box_array, box_count, hole_array, hole_count):
    for (x, y) in hole_array.copy():
        if not level[x][y] == 4:
            level[x][y] = 1
            hole_array.remove((x, y))
            hole_count -= 1
    if hole_count < box_count:
        # add holes on random tiles until we have the correct amount
        floor_tiles = []
        for i in range(size):
            for j in range(size):
                if level[i][j] == 1:
                    floor_tiles.append((i, j))
        random.shuffle(floor_tiles)
        i = 0
        while hole_count < box_count:
            if floor_tiles[i] not in hole_array:
                floor_tiles[i] = 4
                hole_array.append((x,y))
                hole_count += 1
            i += 1
    elif hole_count > box_count:
        # remove holes at random until we have the correct amount
        random.shuffle(hole_array)
        while hole_count > box_count:
            pos = hole_array.pop()
            level[pos[0]][pos[1]] = 1
            hole_count -= 1
    for (x, y) in box_array.copy():
        # remove invalid boxes
        if not level[x][y] == 1:
            box_array.remove((x,y))
    if len(box_array) < box_count:
        floor_tiles = []
        for i in range(size):
            for j in range(size):
                if level[i][j] == 1:
                    floor_tiles.append((i, j))
        random.shuffle(floor_tiles)
        counter = 0
        while len(box_array) < box_count:
            if floor_tiles[counter] not in box_array:
                box_array.append(floor_tiles[counter])
            counter += 1
    not_valid = False
    count = 0
    floor_tiles = []
    for i in range(size):
        for j in range(size):
            if level[i][j] == 1:
                floor_tiles.append((i, j))
    random.shuffle(floor_tiles)
    stack = [floor_tiles[0]]
    while count < size * 2 and not_valid:
        count += 1
        (x,y) = stack.pop()
        if rand() < r_mut:
            r = rand()
            if r < 0.3:
                if level[x][y] == 1:
                    if (x, y) in box_array:
                        random.shuffle(floor_tiles)
                        box_array.remove((x,y))
                        counter = 0
                        while floor_tiles[counter] in box_array:
                            counter += 1
                        box_array.append(floor_tiles[counter])
                    level[x][y] = 0
                elif level[x][y] == 0:
                    level[x][y] = 1
                else:
                    if level[x][y] == 4:
                        random.shuffle(floor_tiles)
                        counter = 0
                        while floor_tiles[counter] in box_array:
                            counter += 1
                        floor_tiles[counter] = 4
                    level[x][y] = 0
            elif r < 0.35:
                level[x][y] = 2
            elif r < 0.4:
                level[x][y] = 4
                random.shuffle(hole_array)
                hole_array.pop()
                hole_array.append((x,y))
        #add all neighbors to queue
        for i in range(-1, 2, 2):
            if size - 1 > x + i >= 0:
                stack.append((x + i, y))
            if size - 1 > y + i >= 0:
                stack.append((x, y + i))
        #randomly select from queue and start over
        random.shuffle(stack)
        #limit at size * 2 and validate
        if count >= size * 2:
            not_valid = validate(level, size)
    return level, hole_array, box_array


    # for i in range(len(bitstring)):
    #     # check for a mutation
    #     if rand() < r_mut:
    #         # flip the bit
    #         bitstring[i] = 1 - bitstring[i]

def level_array_to_string(arr):
    state = ""
    for row in arr:
        for cell in row:
            state += str(cell) + ";"
        state = state[:-1]
        state += "|"
    state = state[:-1]
    return state


# tests of gen algo
def eval(level_array, hole_loc, box_loc, size):
    level_str = level_array_to_string(level_array)
    t = Tree(box_loc, hole_loc, level_str, size)
    t.MCTS()
    highest_entropy = -1
    for branch in t.roots:
        highest_entropy = max(highest_entropy, branch.data.global_entropy)
    print("entropy", highest_entropy)
    return highest_entropy



# define the total iterations
n_iter = 5
# size max 7
size = 5
# box_count max 4
box_count = 3
# special tiles
special_tiles = 2
# bits
n_bits = size * size
# define the population size
n_pop = 20
# crossover rate
r_cross = 0.9
# mutation rate
r_mut = 1.0 / float(n_bits)
# perform the genetic algorithm search
best, score = genetic_algorithm(eval, n_bits, n_iter, n_pop, r_cross, r_mut, size, box_count, special_tiles)
print('Done!')
print('f(%s) = %f' % (best, score))
