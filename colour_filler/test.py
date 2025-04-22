import random
import copy
from enum import Enum
import string


# ==== Tile Definitions ====
class Tile(Enum):
    EMPTY = 0
    NORMAL = 1
    DISAPPEARING = 2
    PUSH = 3
    HOLE = 4
    GREY_HOLE = 5


WIDTH = 5
HEIGHT = 5
POPULATION_SIZE = 50
MUTATION_RATE = 0.05
GENERATIONS = 100
TARGET_SCORE = 7.5
TOLERANCE = 0.01
NUM_PAIRS = 3  # Number of crate/target pairs (a, b, c, ...)
NUM_GREY_CRATES = 2


# ==== Level Data Structure ====
class Level:
    def __init__(self):
        self.tiles = [[random_tile() for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.crates = {}  # {'a': (x, y), 'b': (x, y), ...}
        self.targets = {}  # {'a': (x, y), 'b': (x, y), ...}
        self.grey_crates = []  # [(x, y), ...]

    def clone(self):
        return copy.deepcopy(self)

    def to_string(self):
        grid = []
        for y in range(HEIGHT):
            row = []
            for x in range(WIDTH):
                tile_value = str(self.tiles[y][x].value)
                # Check for crates/targets on this tile
                suffix = ""
                for label, (cx, cy) in self.crates.items():
                    if (x, y) == (cx, cy):
                        suffix += label
                for label, (tx, ty) in self.targets.items():
                    if (x, y) == (tx, ty):
                        suffix += label
                for (gx, gy) in self.grey_crates:
                    if (x, y) == (gx, gy):
                        suffix += "p"
                row.append(tile_value + suffix)
            grid.append(";".join(row))
        return "|".join(grid)


# ==== Helpers ====
def random_tile():
    return random.choice(list(Tile))


def random_position():
    return (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))


def place_objects(level):
    used_positions = set()
    labels = string.ascii_lowercase

    # Place crate-target pairs
    for i in range(NUM_PAIRS):
        label = labels[i]

        while True:
            crate_pos = random_position()
            if crate_pos not in used_positions:
                break
        used_positions.add(crate_pos)
        level.crates[label] = crate_pos

        while True:
            target_pos = random_position()
            if target_pos not in used_positions:
                break
        used_positions.add(target_pos)
        level.targets[label] = target_pos

    # Place grey crates
    for _ in range(NUM_GREY_CRATES):
        while True:
            grey_pos = random_position()
            if grey_pos not in used_positions:
                break
        used_positions.add(grey_pos)
        level.grey_crates.append(grey_pos)


def create_random_level():
    level = Level()
    place_objects(level)
    return level


def mutate(level):
    new_level = level.clone()

    # Mutate tiles
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if random.random() < MUTATION_RATE:
                new_level.tiles[y][x] = random_tile()

    # Mutate crate positions
    for label in new_level.crates:
        if random.random() < MUTATION_RATE:
            new_level.crates[label] = random_position()

    # Mutate target positions
    for label in new_level.targets:
        if random.random() < MUTATION_RATE:
            new_level.targets[label] = random_position()

    # Mutate grey crate positions
    for i in range(len(new_level.grey_crates)):
        if random.random() < MUTATION_RATE:
            new_level.grey_crates[i] = random_position()

    return new_level


def crossover(parent1, parent2):
    child = Level()

    # Crossover tiles
    for y in range(HEIGHT):
        for x in range(WIDTH):
            child.tiles[y][x] = random.choice([parent1.tiles[y][x], parent2.tiles[y][x]])

    # Crossover crates and targets
    for label in parent1.crates:
        child.crates[label] = random.choice([parent1.crates[label], parent2.crates[label]])
        child.targets[label] = random.choice([parent1.targets[label], parent2.targets[label]])

    # Crossover grey crates
    child.grey_crates = random.sample(
        parent1.grey_crates + parent2.grey_crates, NUM_GREY_CRATES
    )

    return child


def fitness(level):
    score = evaluate_level(level.to_string())
    return -abs(score - TARGET_SCORE)


# ==== Placeholder for your real evaluation ====
def evaluate_level(level_string):
    # Replace with your actual scoring logic
    wall_count = level_string.count("0")
    total_tiles = WIDTH * HEIGHT
    wall_ratio = wall_count / total_tiles
    return wall_ratio * 10


# ==== Main Genetic Algorithm ====
def genetic_algorithm():
    population = [create_random_level() for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        scored_population = [(level, fitness(level)) for level in population]
        scored_population.sort(key=lambda x: x[1], reverse=True)

        best_level, best_fitness = scored_population[0]
        best_score = evaluate_level(best_level.to_string())

        print(f"Generation {generation}: Best score = {best_score:.4f}, Target = {TARGET_SCORE}")

        if abs(best_score - TARGET_SCORE) <= TOLERANCE:
            print("✅ Target achieved!")
            break

        survivors = [level for level, _ in scored_population[:POPULATION_SIZE // 5]]

        new_population = survivors.copy()
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(survivors, 2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population

    print(f"\nBest level score: {best_score}")
    return best_level


# ==== Run the algorithm ====
if __name__ == "__main__":
    best_level = genetic_algorithm()

    print("\nBest Level Layout:")
    print(best_level.to_string())
