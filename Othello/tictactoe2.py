import sys
import math
import time

startTime = time.time()
cache, winnables = {}, []
length = len(sys.argv[1])
if len(sys.argv) > 2: default = int(sys.argv[2])
else:
    temp = math.floor(len(sys.argv[1])**.5)
    while length % temp: temp -= 1
    default = length // temp
invals = [3, length//default, default, length]
winX, winO, counts = 'X' * invals[0], 'O' * invals[0], [sys.argv[1].count('X'), sys.argv[1].count('O')]

def setGlobals(invals):
    for n in range(invals[3]):
        row = list(range(n//invals[2]*invals[2], (n//invals[2]+1)*invals[2]))
        if len(row) >= invals[0] and row not in winnables:
            winnables.append(row)
        column = list(range(n%invals[2], invals[3], invals[2]))
        if len(column) >= invals[0] and column not in winnables:
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
                winnables.append(backward)

def isWon(pzl):
    for r in winnables:
        curr = ''
        for a in r: curr = curr + pzl[a]
        if winX in curr: return 3
        if winO in curr: return 1
    if '.' not in pzl: return 2
    return ''

def bruteForce(pzl):
    if pzl in cache: return cache[pzl]
    result = isWon(pzl)
    if result:
        return result-2
    else:
        poss = []
        for n in range(invals[3]):
            if pzl[n] == '.':
                if counts[0] <= counts[1]: 
                    x = pzl[:n] + 'X' + pzl[n+1:]
                    counts[0] += 1
                    bF = bruteForce(x)
                    poss.append((bF, x))
                    cache[x] = bF
                    counts[0] -= 1
                else:
                    o = pzl[:n] + 'O' + pzl[n+1:]
                    counts[1] += 1
                    bF = bruteForce(o)
                    poss.append((bF, o))
                    cache[o] = bF
                    counts[1] -= 1
        if counts[0] <= counts[1]: return max(poss)[0]
        else: return min(poss)[0]

setGlobals(invals)
pzl = sys.argv[1]
poss = []
for n in range(invals[3]):
    if pzl[n] == '.':
        if counts[0] <= counts[1]: 
            x = pzl[:n] + 'X' + pzl[n+1:]
            counts[0] += 1
            bF = bruteForce(x)
            poss.append((bF, x, n))
            cache[x] = bF
            counts[0] -= 1
        else:
            o = pzl[:n] + 'O' + pzl[n+1:]
            counts[1] += 1
            bF = bruteForce(o)
            poss.append((-bF, o, n))
            cache[o] = bF
            counts[1] -= 1
poss.sort()
print(*poss, sep='\n')