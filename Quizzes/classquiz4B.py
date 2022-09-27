import time
import math
import sys

def q2(x):
    for i in range(len(x)):
        if x[i] != '_' and int(x[i]) == i+1:
            return False
    return True

def find(puzzle):
    duals = [[] for x in range(5)]
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
            if x in levels and levels[x] == levels[puzzle]+1:
                pre = False
                for i in range(len(duals)):
                    if x in duals[i]:
                        duals[i].remove(x)
                        duals[i+1].append(x)
                        pre = True
                        break
                if not pre:
                    duals[0].append(x)
            if x not in collect:
                lev = levels[puzzle] + 1
                levels[x] = lev
                parseMe.append(x)
                collect[x] = puzzle
        n = n + 1
    total = 0
    for i, n in enumerate(duals):
        num = len(n)
        total += num
        print(i+2, ': ', num, sep='')
    print(total)
    print()
find("12345678_")
find("1234567_8")
find("1234_5678")