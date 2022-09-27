import time
import math
import sys

def q2(x):
    for i in range(len(x)):
        if x[i] != '_' and int(x[i]) == i+1:
            return False
    return True

def find(puzzle):
    leaves = [[] for x in range(32)]
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
        leaves[levels[puzzle]].append(puzzle)
        for x in a:
            if x not in collect:
                lev = levels[puzzle] + 1
                if len(leaves[levels[puzzle]]) > 0:
                    leaves[levels[puzzle]].pop()
                levels[x] = lev
                parseMe.append(x)
                collect[x] = puzzle
        n = n + 1
    total = 0
    close_leaf = []
    close_dist = -1
    far_no_leaf = -1
    print()
    for i, n in enumerate(leaves):
        num = len(n)
        if num == 0:
            far_no_leaf = i
        if num > 0 and close_dist == -1:
            close_leaf = n
            close_dist = i
        total += num
        print(i, ': ', num, sep='')
    print()
    print(total)
    print()
    print(far_no_leaf)
    print()
    print(close_dist)
    print()
    print(close_leaf)

find("12345678_")
find("1234567_8")
find("1234_5678")