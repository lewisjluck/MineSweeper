from random import random

def getGrid(dimensions, pointer):
    p = [pointer, pointer - 1, pointer + 1, pointer - dimensions, ]
    grid = []
    for i in range(dimensions*dimensions):
        if round(random()*3) == 0 and i not in p:
            grid.append('*')
        else:
            grid.append(0)

    for i in range(len(grid)):
        if grid[i] != '*':
            tally = 0
            if i%dimensions != 0:
                if grid[i-1] == '*':
                    tally += 1
            if i%dimensions != dimensions-1:
                if grid[i+1] == '*':
                    tally += 1
            if i >= dimensions:
                if grid[i-dimensions] == '*':
                    tally += 1
                if i%dimensions != 0:
                    if grid[i-dimensions-1] == '*':
                        tally += 1
                if i%dimensions != dimensions-1:
                    if grid[i-dimensions+1] == '*':
                        tally += 1
            if i < dimensions*dimensions - dimensions:
                if grid[i+dimensions] == '*':
                    tally += 1
                if i%dimensions != 0:
                    if grid[i+dimensions-1] == '*':
                        tally += 1
                if i%dimensions != dimensions-1:
                    if grid[i+dimensions+1] == '*':
                        tally += 1
            grid[i] = tally

    for i in range(len(grid)):
        if i%dimensions == dimensions-1:
            print(grid[i])
        else:
            print(grid[i], end=" ")
    return grid
