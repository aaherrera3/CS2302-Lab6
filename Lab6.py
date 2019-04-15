# Lab 6
# Programmed by Anthon Herrera
# Last modified April, 14, 2019

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import random
import time


def DisjointSetForest(size):
    return np.zeros(size, dtype=np.int) - 1


def dsfToSetList(S):
    # Returns aa list containing the sets encoded in S
    sets = [[] for i in range(len(S))]
    for i in range(len(S)):
        sets[find(S, i)].append(i)
    sets = [x for x in sets if x != []]
    return sets


def find(S, i):
    # Returns root of tree that i belongs to
    if S[i] < 0:
        return i
    return find(S, S[i])


def find_c(S, i):  # Find with path compression
    if S[i] < 0:
        return i
    r = find_c(S, S[i])
    S[i] = r
    return r


def union(S, i, j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S, i)
    rj = find(S, j)
    if ri != rj:
        S[rj] = ri


def union_c(S, i, j):
    # Joins i's tree and j's tree, if they are different
    # Uses path compression
    ri = find_c(S, i)
    rj = find_c(S, j)
    if ri != rj:
        S[rj] = ri


def union_by_size(S, i, j):
    # if i is a root, S[i] = -number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree
    # Uses path compression
    ri = find_c(S, i)
    rj = find_c(S, j)
    if ri != rj:
        if S[ri] > S[rj]:  # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri


def draw_dsf(S):
    scale = 30
    fig, ax = plt.subplots()
    for i in range(len(S)):
        if S[i] < 0:  # i is a root
            ax.plot([i * scale, i * scale], [0, scale], linewidth=1, color='k')
            ax.plot([i * scale - 1, i * scale, i * scale + 1], [scale - 2, scale, scale - 2], linewidth=1, color='k')
        else:
            x = np.linspace(i * scale, S[i] * scale)
            x0 = np.linspace(i * scale, S[i] * scale, num=5)
            diff = np.abs(S[i] - i)
            if diff == 1:  # i and S[i] are neighbors; draw straight line
                y0 = [0, 0, 0, 0, 0]
            else:  # i and S[i] are not neighbors; draw arc
                y0 = [0, -6 * diff, -8 * diff, -6 * diff, 0]
            f = interpolate.interp1d(x0, y0, kind='cubic')
            y = f(x)
            ax.plot(x, y, linewidth=1, color='k')
            ax.plot([x0[2] + 2 * np.sign(i - S[i]), x0[2], x0[2] + 2 * np.sign(i - S[i])],
                    [y0[2] - 1, y0[2], y0[2] + 1], linewidth=1, color='k')
        ax.text(i * scale, 0, str(i), size=20, ha="center", va="center",
                bbox=dict(facecolor='w', boxstyle="circle"))
    ax.axis('off')
    ax.set_aspect(1.0)

def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off')
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w


def NumberOfSets(S):# will count the number of -1 that show diffrent sets
    count = 0
    for x in S:
        if x == -1:
            count += 1
    return count

plt.close("all")
maze_rows = 10
maze_cols = 15

walls = wall_list(maze_rows,maze_cols)

draw_maze(walls,maze_rows,maze_cols,cell_nums=True)

disjoint_set_forest = DisjointSetForest(maze_rows*maze_cols)

number_of_set = NumberOfSets(disjoint_set_forest)

print('Maze using union')
timer_0 = time.time()
while number_of_set > 1:                                                                # will create the maze using stander union of sets
    choice = random.choice(walls) # selects random wall from list
    index = walls.index(choice)  # return index of wall
    if find(disjoint_set_forest,choice[0]) != find(disjoint_set_forest,choice[1]):
        walls.pop(index) # deletes the wall selected
        union(disjoint_set_forest,choice[0],choice[1]) # add the wall to a set using union
        number_of_set -= 1 # decreases the number of sets by one
timer_1 = time.time()
print('Total time ', timer_1-timer_0)

draw_maze(walls,maze_rows,maze_cols)

#########################################################################################################
maze_rows = 10
maze_cols = 15

walls = wall_list(maze_rows,maze_cols)

draw_maze(walls,maze_rows,maze_cols,cell_nums=True)

disjoint_set_forest = DisjointSetForest(maze_rows*maze_cols)

number_of_set = NumberOfSets(disjoint_set_forest)

print('Maze using union compression ')
timer_0 = time.time()
while number_of_set > 1:                                                                    #Will create the maze using union with compression
    choice = random.choice(walls) # selects random wall from list
    index = walls.index(choice)  # return index of wall
    if find(disjoint_set_forest,choice[0]) != find(disjoint_set_forest,choice[1]):
        walls.pop(index) # deletes the wall selected
        union_c(disjoint_set_forest,choice[0],choice[1]) # add the wall to a set using union compression
        number_of_set -= 1 # decreases the number of sets by one
timer_1 = time.time()
print('Total time ', timer_1-timer_0)
draw_maze(walls,maze_rows,maze_cols)
##################################################################################
maze_rows = 10
maze_cols = 15

walls = wall_list(maze_rows,maze_cols)

draw_maze(walls,maze_rows,maze_cols,cell_nums=True)

disjoint_set_forest = DisjointSetForest(maze_rows*maze_cols)

number_of_set = NumberOfSets(disjoint_set_forest)

print('Maze using union by size compression')
timer_0 = time.time()
while number_of_set > 1:                                                                    #Will create the maze using union by size  with compression
    choice = random.choice(walls) # selects random wall from list
    index = walls.index(choice) # return index of wall
    if find(disjoint_set_forest,choice[0]) != find(disjoint_set_forest,choice[1]):
        walls.pop(index) # deletes the wall selected
        union_by_size(disjoint_set_forest,choice[0],choice[1]) # add the wall to a set using union by size compression
        number_of_set -= 1 # decreases the number of sets by one
timer_1 = time.time()
print('Total time ', timer_1-timer_0)

draw_maze(walls,maze_rows,maze_cols)
plt.show()