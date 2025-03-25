# genetic algorithm
import random

from numpy.random import randint, rand

from tree_structure.Tree import Tree



def genetic_algorithm(objective, n_bits, n_iter, n_pop, r_cross, r_mut, size, box_count):
    # number of boxes, disappearing tiles, push tiles, level size (floor spaces)
    # initial population of random bitstring
    # size * size array
    # pop = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]
    pop = [generate(size, box_count) for _ in range(n_pop)]
    # keep track of best solution
    best, best_eval = 0, objective(pop[0])
    # enumerate generations
    for gen in range(n_iter):
        # evaluate all candidates in the population
        scores = [objective(c) for c in pop]
        # check for new best solution
        for i in range(n_pop):
            if scores[i] < best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %.3f" % (gen, pop[i], scores[i]))
        # select parents
        selected = [selection(pop, scores) for _ in range(n_pop)]
        # create the next generation
        children = list()
        for i in range(0, n_pop, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i + 1]
            # crossover and mutation
            for c in crossover(p1, p2, r_cross):
                # mutation
                mutation(c, r_mut)
                # store for next generation
                children.append(c)
        # replace population
        pop = children
    return [best, best_eval]

def generate(size, box_count):
    generated = [[0 for i in range(size)] for j in range(size)]
    x, y = int(randint(size)/2), int(randint(size)/2)
    generated[x][y] = 1
    flipped = 0
    stack = [(x,y)]
    while True:
        (x, y) = stack.pop()
        for i in range(-1, 2, 2):
            if size-1 > x > 0 and generated[x + i][y] == 0:
                generated[x + i][y] = 1
                flipped += 1
            if size-1 > y > 0 and generated[x][y + i] == 0:
                generated[x][y + i] = 1
                flipped += 1
            if size-1 > x+i >= 0:
                stack.append((x + i, y))
            if size-1 > y+i >= 0:
                stack.append((x, y + i))
            random.shuffle(stack)
        if flipped > 0.6 * size*size:
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
    hole_locations = floor_tiles[:box_count]
    box_locations = []

    #TODO: add box location generation
    return generated, hole_locations, box_locations

def validate(level, size):
    list_of_coords = []
    for i in range(size):
        for j in range(size):
            if int(level[i][j]) > 0:
                if len(list_of_coords) == 0:
                    list_of_coords.extend(DFS(level, (i,j), size))
                elif (i,j) not in list_of_coords:
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
    selection_ix = randint(len(pop))
    for ix in randint(0, len(pop), k - 1):
        # check if better (e.g. perform a tournament)
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]


# crossover two parents to create two children
def crossover(p1, p2, r_cross):
    # children are copies of parents by default
    c1, c2 = p1.copy(), p2.copy()
    # check for recombination
    if rand() < r_cross:
        # select crossover point that is not on the end of the string
        pt = randint(1, len(p1) - 2)
        # perform crossover
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]


# mutation operator
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        # check for a mutation
        if rand() < r_mut:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]


# tests of gen algo
def eval(levelstr, hole_loc, box_loc):
    t = Tree()
    t.MCTS()


# objective function
def onemax(x):
    return -sum(x)


# define the total iterations
n_iter = 100
# bits
n_bits = 20
# define the population size
n_pop = 100
# crossover rate
r_cross = 0.9
# mutation rate
r_mut = 1.0 / float(n_bits)
# perform the genetic algorithm search
best, score = genetic_algorithm(onemax, n_bits, n_iter, n_pop, r_cross, r_mut, 5, 3)
print('Done!')
print('f(%s) = %f' % (best, score))
