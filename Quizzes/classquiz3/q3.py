import time
import math
import sys

def q2(x):
    for i in range(len(x)):
        if x[i] != '_' and int(x[i]) == i+1:
            return False
    return True

def find(puzzle):
    tracker = ''
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
                if q2(x):
                    tracker = x

        n = n + 1
    while tracker != '':
        print(tracker)
        tracker = collect[tracker]
    print(levels[x])

find("12345678_")