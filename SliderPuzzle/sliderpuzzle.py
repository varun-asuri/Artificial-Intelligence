import time
import math
import sys

def solve(puzzle, goal):
    size = int(math.sqrt(len(puzzle)))
    parseMe = [puzzle]
    dictionary = {puzzle:""}
    n = 0
    while parseMe:
        if n >= len(parseMe):
            break
        puzzle = parseMe[n]
        if puzzle == goal:
            a = []
            x = puzzle
            while x != "":
                a.append(x)
                x = dictionary[x]
            print("Steps: " + str(len(a)-1))
            return ""
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
            if x not in dictionary:
                parseMe.append(x)
                dictionary[x] = puzzle
        n = n + 1
    print("Steps: " + str(-1))

if len(sys.argv) == 2:
    solve(sys.argv[1], "12345678_")
else:
    solve(sys.argv[1], sys.argv[2])