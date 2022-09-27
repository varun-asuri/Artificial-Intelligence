import time
import math
import sys

def solve(puzzle, goal):
    initial = puzzle
    startTime = time.time()
    size = int(math.sqrt(len(puzzle)))
    parseMe = [puzzle]
    dictionary = {puzzle:""}
    n = 0
    farthest = ''
    while parseMe:
        if n >= len(parseMe):
            break
        puzzle = parseMe[n]
        farthest = puzzle
        if puzzle == goal:
            a = []
            x = puzzle
            while x != "":
                a.append(x)
                x = dictionary[x]
            a = a[::-1]
            b = []
            c = 0
            div, mod = divmod(len(a), 10)
            if mod:
                c = 1
            for x in range(div+c):
                d = a[x*10:min(len(a), x*10+10)]
                b.append(d)
            for x in b:
                for num in range(size):
                    for index in range(len(x)):
                        print(x[index][int(num*size):int(num*size+size)], end = "  ")
                    print()
                print()
            print()
            print("Distance: " + str(len(a)-1))
            print()
            totalTime = time.time()-startTime
            print("Time: " + str(totalTime)[:4] + "s")
            print()
            print('-----------------------------------')
            print()
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
    init = [initial]
    for num in range(size):
        for index in range(len(init)):
            print(init[index][int(num*size):int(num*size+size)], end = "  ")
        print()
    print()
    totalTime = time.time()-startTime
    print("Distance: " + str(-1))
    print()
    print("Time: " + str(totalTime)[:4] + "s")
    print()
    print('-----------------------------------')
    print()
    return farthest

resolv = ''
if len(sys.argv) == 2:
    resolv = solve(sys.argv[1], "12345678_")
else:
    resolv = solve(sys.argv[1], sys.argv[2])
solve(sys.argv[1], resolv)