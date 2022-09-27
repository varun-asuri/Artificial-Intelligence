import time
import math
import sys
import random

startTime = time.time()
SYMSET = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
LOOKUP = [0, 0, [], 0, 0, []]

def setGlobals(pzl):
    LOOKUP[0] = len(pzl)
    LOOKUP[1] = int(LOOKUP[0]**.5)
    LOOKUP[2] = [-1]
    LOOKUP[3] = math.floor(LOOKUP[1]**.5)
    while LOOKUP[1] % LOOKUP[3] != 0: LOOKUP[3] -= 1
    LOOKUP[4] = LOOKUP[1] // LOOKUP[3]
    LOOKUP[5] = []
    for indx in range(LOOKUP[0]):
        nbrs = set()
        for n in range(LOOKUP[1]):
            nbrs.add((indx//LOOKUP[1])*LOOKUP[1]+n)
            nbrs.add(indx%LOOKUP[1]+n*LOOKUP[1])
            nbrs.add((indx//(LOOKUP[1]*LOOKUP[3]))*(LOOKUP[1]*LOOKUP[3])+((indx//LOOKUP[4])*LOOKUP[4])%LOOKUP[1]+n%LOOKUP[4]+(n//LOOKUP[4])*LOOKUP[1])
        nbrs.remove(indx)
        LOOKUP[5].append(nbrs)

def printFormat(pzl):
    for n3 in range(LOOKUP[1]):
        print(pzl[n3*LOOKUP[1]:n3*LOOKUP[1]+LOOKUP[1]])

def isInvalid(pzl):
    if LOOKUP[2][-1] == -1:
        for indx in range(LOOKUP[0]):
            if pzl[indx] == '.': continue
            for pos in LOOKUP[5][indx]:
                if pzl[indx] == pzl[pos]: return True
    else:
        for pos in LOOKUP[5][LOOKUP[2][-1]]:
            if pzl[LOOKUP[2][-1]] == pzl[pos]: return True
    return False
    
def bruteForce(pzl):
    if isInvalid(pzl): return ''
    if '.' not in pzl: return pzl
    
    LOOKUP[2].append(pzl.index('.'))
    setOfChoices = []
    for poss in range(LOOKUP[1]):
        setOfChoices.append(pzl[0:LOOKUP[2][-1]]+SYMSET[poss]+pzl[LOOKUP[2][-1]+1:]) 
    for subPzl in setOfChoices:
        bF = bruteForce(subPzl)
        if bF: return bF
    LOOKUP[2].pop()
    return ''

filename = sys.argv[1]
PZLS = open(filename, 'r').read().splitlines()
for indx, start in enumerate(PZLS):
    if time.time()-startTime > 60 or indx == 51: break
    print('\nPuzzle ', indx+1, ':\n', start, sep='')
    setGlobals(start)
    s = bruteForce(start)
    if s == '': print('No solution possible')
    else: print(s)

# print(START)
# s = bruteForce(START)
# if s == '': print('No solution possible')
# else: print(s)

print('\nTime: ', time.time()-startTime, 's', sep='')