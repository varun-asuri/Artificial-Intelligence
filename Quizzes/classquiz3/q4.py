import time
import math
import sys

def find(puzzle):
    counter = 181440
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
        checker = False
        if puzzle[4] == '_':
            checker = True
        for x in a:
            if x[4] == '_':
                checker = True
        if checker:
            counter -= 1
        for x in a:
            if x not in collect:
                lev = levels[puzzle]+1
                levels[x] = lev
                parseMe.append(x)
                collect[x] = puzzle

        n = n + 1
    print(counter)

find("12345678_")