import time
import math
import sys

def q1(x):
    dx = {}
    for i in range(len(x)):
        if x[i] == '_':
            dx[i] = x[i]
        else:
            dx[i] = int(x[i])
    if dx[0] != '_' and (dx[0] + 1 == dx[1] or dx[0] - 1 == dx[1] or dx[0] + 1 == dx[3] or dx[0] - 1 == dx[3]):
        return False
    if dx[2] != '_' and (dx[2] + 1 == dx[1] or dx[2] - 1 == dx[1] or dx[2] + 1 == dx[5] or dx[2] - 1 == dx[5]):
        return False
    if dx[6] != '_' and (dx[6] + 1 == dx[7] or dx[6] - 1 == dx[7] or dx[6] + 1 == dx[3] or dx[6] - 1 == dx[3]):
        return False
    if dx[8] != '_' and (dx[8] + 1 == dx[7] or dx[8] - 1 == dx[7] or dx[8] + 1 == dx[5] or dx[8] - 1 == dx[5]):
        return False
    if dx[4] != '_' and (dx[4] + 1 == dx[3] or dx[4] - 1 == dx[3] or dx[4] + 1 == dx[5] or dx[4] - 1 == dx[5] or dx[4] + 1 == dx[1] or dx[4] - 1 == dx[1] or dx[4] + 1 == dx[7] or dx[4] - 1 == dx[7]):
        return False
    return True

def find(puzzle):
    size = int(math.sqrt(len(puzzle)))
    parseMe = [puzzle]
    collect = {puzzle:''}
    levels = {puzzle:0}
    n = 0
    while parseMe:
        if n >= len(parseMe):
            break
        puzzle = parseMe[n]
        a = []
        b = puzzle.index("_")
        if b > size-1:
            a.append( puzzle[0: b-size] + puzzle[b] + puzzle[b-size+1:b] + puzzle[b-size] + puzzle[b+1:] )
        if b > 0 and b % size:
            a.append( puzzle[0: b-1] + puzzle[b] + puzzle[b-1] + puzzle[b+1:] )
        if b < len(puzzle)-1 and b % size != size-1:
            a.append( puzzle[0: b] + puzzle[b+1] + puzzle[b] + puzzle[b+2:] )
        if b < len(puzzle)-size:
            a.append( puzzle[0: b] + puzzle[b+size] + puzzle[b+1:b+size] + puzzle[b] + puzzle[b+size+1:] )
        for x in a:
            if x not in collect:
                lev = levels[puzzle]+1
                levels[x] = lev
                parseMe.append(x)
                collect[x] = puzzle
                if q1(x):
                    while x != '':
                        print(x)
                        x = collect[x]
                    print(lev)
                    n = 1000000

        n = n + 1

find("12345678_")