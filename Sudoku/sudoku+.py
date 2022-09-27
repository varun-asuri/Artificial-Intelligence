#Varun Asuri 1481167
import time
import math
import sys
import random

startTime = time.time()
SYMSET = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
LOOKUP = [0, 0, 0, 0, [], set(), set()]

def setGlobals(pzl):
    LOOKUP[0] = len(pzl) #length of the string pzl at any given point
    LOOKUP[1] = int(LOOKUP[0]**.5) #number of each type of constrain set (rows, columns, blocks)
    LOOKUP[2] = math.floor(LOOKUP[1]**.5) 
    while LOOKUP[1] % LOOKUP[2] != 0: LOOKUP[2] -= 1 #height of each sub-block
    LOOKUP[3] = LOOKUP[1] // LOOKUP[2] #width of each sub-block
    LOOKUP[4] = [] #an array of neighboring indices for any given index in the puzzle
    for indx in range(LOOKUP[0]):
        nbrs = set()
        for n in range(LOOKUP[1]):
            nbrs.add((indx//LOOKUP[1])*LOOKUP[1]+n)
            nbrs.add(indx%LOOKUP[1]+n*LOOKUP[1])
            nbrs.add((indx//(LOOKUP[1]*LOOKUP[2]))*(LOOKUP[1]*LOOKUP[2])+((indx//LOOKUP[3])*LOOKUP[3])%LOOKUP[1]+n%LOOKUP[3]+(n//LOOKUP[3])*LOOKUP[1])
        nbrs.remove(indx)
        LOOKUP[4].append(nbrs)
    for n in SYMSET[:LOOKUP[1]]:
        LOOKUP[5].add(n) #the relevant SYMSET for this puzzle

def findIndex(pzl):
    pIndex = (math.inf, set(), -1) #a dummy initial value that will be replaced by min
    for x in LOOKUP[6]: #see line 69
        nbrs = LOOKUP[4][x] #all neighboring indices for that period
        posSyms = set()
        for nbr in nbrs:
            posSyms.add(pzl[nbr]) #all characters from the SYMSET it shares a constraint with
        posSyms = LOOKUP[5] - posSyms #complement of that or all possible characters for that position
        n = len(posSyms)
        if n < 2: return (n, posSyms, x) #bail if there is no possible or only one possible character
        pIndex = min( pIndex, (n, posSyms, x) )
    return pIndex #by the end pIndex will have the index with the least amount of characters available

def bruteForce(pzl):
    if '.' not in pzl: return pzl
    t = findIndex(pzl) #t is a tuple of (number of possible characters, possible characters, period index)
    if t[0]:
        LOOKUP[6].remove(t[2]) #that index will no longer have a period
        for poss in t[1]:
            bF = bruteForce(pzl[0:t[2]]+poss+pzl[t[2]+1:])
            if bF: return bF
        LOOKUP[6].add(t[2]) #if I get to this point it obviously didn't work so it is a period once more
    return ''

def checkSum(pzl):
    n = 0
    for x in pzl:
        n += int(x)
    print(n)

prev = ''
filename = sys.argv[1]
PZLS = open(filename, 'r').read().splitlines() #it is a list of all puzzles
for indx, start in enumerate(PZLS):
    print('\nPuzzle ', indx+1, ':\n', start, sep='')
    if len(prev) != len(start): #if it has the same dimensions as the last puzzle I don't need setGlobals
        setGlobals(start)
    prev = start
    for x in range(len(start)):
        if start[x] == '.':
            LOOKUP[6].add(x) #this is a list of all periods in the puzzle
    s = bruteForce(start)
    if s == '': print('No solution possible')
    else: print(s)
    checkSum(s)

print('\nTime: ', time.time()-startTime, 's', sep='')