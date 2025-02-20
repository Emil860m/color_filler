from random import randrange


def generate_grid_cellular_auto(size):
    grid = [["0" for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(size):
            if randrange(0, 10) < 5:
                grid[i][j] = "1"
    for i in range(3):
        grid = game_of_life_gen(grid, size)
        for i in range(size):
            for j in range(size):
                print(grid[i][j], end="")
            print("")
        print("-------------")

def game_of_life_gen(grid, size):
    for i in range(size):
        for j in range(size):
            i_lower = i-1
            i_upper = i+1
            j_lower = j-1
            j_upper = j+1
            if i == 0:
                i_lower = 0
            if j == 0:
                j_lower = 0
            if i == size-1:
                i_upper = size-1
            if j == size-1:
                j_upper = size-1
            counter = 0
            for k in range(i_lower, i_upper+1):
                for l in range(j_lower, j_upper+1):
                    if not (i == k and j == l):
                        print(i,j,k,l, grid[k][l])
                        counter = counter + int(grid[k][l])
            if grid[i][j] == "0" and counter > 0:
                grid[i][j] = "1"
            if grid[i][j] == "1" and (counter < 1 or counter > 3):
                grid[i][j] = "0"
            print(i, j, counter)
    print(grid)
    return grid



generate_grid_cellular_auto(10)