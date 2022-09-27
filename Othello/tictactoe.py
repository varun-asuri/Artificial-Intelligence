import sys
import math
import time

startTime = time.time()
finals, cache, winnables = [set(), set(), set()], {}, []
invals = [int(sys.argv[1])]
if sys.argv[2] > sys.argv[3]:
    invals.append(int(sys.argv[3]))
    invals.append(int(sys.argv[2]))
else:
    invals.append(int(sys.argv[2]))
    invals.append(int(sys.argv[3]))
invals.append(invals[1]*invals[2])
winX, winO, counts = 'X' * invals[0], 'O' * invals[0], [0, 0]

def setGlobals(invals):
    print('\nConstraints:', end=' ')
    for n in range(invals[3]):
        row = list(range(n//invals[2]*invals[2], (n//invals[2]+1)*invals[2]))
        if len(row) >= invals[0] and row not in winnables:
            print(row, end=' ')
            winnables.append(row)
        column = list(range(n%invals[2], invals[3], invals[2]))
        if len(column) >= invals[0] and column not in winnables:
            print(column, end=' ')
            winnables.append(column)
        if not n%invals[2] in [0,invals[2]-1] or n//invals[2] in [0, invals[1]]:
            forward = []
            for x in range(n,invals[3],invals[2]+1):
                forward.append(x)
                if not (x+1)%invals[2]: break
            for x in range(n-invals[2]-1,-1,-invals[2]-1):
                if not (x+1)%invals[2]: break
                forward.append(x)
            forward.sort()
            if len(forward) >= invals[0] and forward not in winnables:
                print(forward, end=' ')
                winnables.append(forward)
            backward = []
            for x in range(n,invals[3],invals[2]-1):
                backward.append(x)
                if not x%invals[2]: break
            for x in range(n-invals[2]+1,-1,-invals[2]+1):
                if not x%invals[2]: break
                backward.append(x)
            backward.sort()
            if len(backward) >= invals[0] and backward not in winnables:
                print(backward, end=' ')
                winnables.append(backward)
    print('\nConstruction Time: ', time.time()-startTime, 's', sep='')
    print('____________\n')

def isWon(pzl):
    for r in winnables:
        curr = ''
        for a in r: curr = curr + pzl[a]
        if winX in curr: return 2
        if winO in curr: return 3
    if '.' not in pzl: return 1
    return ''

def bruteForce(pzl):
    if pzl in cache: return cache[pzl]
    result = isWon(pzl)
    if result:
        finals[result-1].add(pzl)
        return 1
    else:
        poss = []
        for n in range(invals[3]):
            if pzl[n] == '.':
                if counts[0] <= counts[1]: 
                    x = pzl[:n] + 'X' + pzl[n+1:]
                    counts[0] += 1
                    poss.append(bruteForce(x))
                    cache[x] = poss[-1]
                    counts[0] -= 1
                else:
                    o = pzl[:n] + 'O' + pzl[n+1:]
                    counts[1] += 1
                    poss.append(bruteForce(o))
                    cache[o] = poss[-1]
                    counts[1] -= 1
        return sum(poss)

def printFormat(games):
    print('Possible Games:', games)
    print('Total Puzzles:', len(cache))
    print('Terminal Puzzles:', len(finals[1])+len(finals[2])+len(finals[0]))
    print('Wins for X:', len(finals[1]))
    print('Wins for O:', len(finals[2]))
    print('Ties:', len(finals[0]))
    print('____________\n')
    print('Time: ', time.time()-startTime, 's', sep='')

setGlobals(invals)
pzl = '.' * invals[3]
games = bruteForce(pzl)
cache[pzl] = games
printFormat(games)