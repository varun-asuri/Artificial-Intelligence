import sys
import math

def neighbors(puzzle):
    a = []
    b = puzzle.index("_")
    if b > 2:
        a.append( puzzle[0: b-3] + puzzle[b] + puzzle[b-2:b] + puzzle[b-3] + puzzle[b+1:] )
    if b > 0 and b % 3:
        a.append( puzzle[0: b-1] + puzzle[b] + puzzle[b-1] + puzzle[b+1:] )
    if b < len(puzzle)-1 and b % 3 != 2:
        a.append( puzzle[0: b] + puzzle[b+1] + puzzle[b] + puzzle[b+2:] )
    if b < len(puzzle)-3:
        a.append( puzzle[0: b] + puzzle[b+3] + puzzle[b+1:b+3] + puzzle[b] + puzzle[b+4:] )
    return a
def solve(puzzle):
    initial = puzzle
    archive = set()
    parseMe = [puzzle]
    count = 0
    n = 0
    while parseMe:
        print(str(count) + ': ' + str(len(parseMe)))
        n += len(parseMe)
        copy = []
        for puzzle in parseMe:
            a = neighbors(puzzle)
            for x in a:
                if x not in archive and x != initial:
                    copy.append(x)
                    archive.add(x)
        parseMe = copy
        count += 1
    print('Total: ' + str(n))
solve(sys.argv[1])