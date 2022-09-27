#Varun Asuri 1481167
import time
import math
import sys
import random

startTime = time.time()
SYMSET = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
LOOKUP = [0, 0, 0, 0, [], set(), {}, []]

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

def copyPeriods(): #returns full deep copy of LOOKUP[6]
    copyBuffer = {}
    for x in LOOKUP[6]:
        copyBuffer[x] = {*LOOKUP[6][x]} #use the asterisk operator to copy sets
    return copyBuffer

def rippleEffect(sym, indx):
    LOOKUP[7].append(copyPeriods()) #I store the current settings in this array as a stack
    for x in LOOKUP[4][indx] & LOOKUP[6].keys(): #I search in the intersection because those are the only ones affected
        if sym in LOOKUP[6][x]:
            LOOKUP[6][x].remove(sym) #I remove as it is no longer usable
            if len(LOOKUP[6][x]) == 0: return False #if that period can no longer have a value it is an impossible situation
    return True #default return

def findIndex(pzl):
    pIndex = (math.inf, set(), -1) #a dummy initial value that will be replaced by min
    for x, posSyms in LOOKUP[6].items(): #see line 80
        n = len(posSyms)
        if n < 2: return (n, posSyms, x) #bail if there is no possible or only one possible character
        pIndex = min( pIndex, (n, posSyms, x) )
    return pIndex #by the end pIndex will have the index with the least amount of characters available

def bruteForce(pzl):
    if '.' not in pzl: return pzl
    t = findIndex(pzl) #t is a tuple of (number of possible characters, possible characters, period index)
    if t[0]:
        LOOKUP[6].pop(t[2]) #that index will no longer have a period
        for poss in t[1]:
            if rippleEffect(poss, t[2]): #periods that share a constrain need to update since they can no longer use this value
                bF = bruteForce(pzl[0:t[2]]+poss+pzl[t[2]+1:])
                if bF: return bF
            LOOKUP[6] = LOOKUP[7].pop() #revert back by restoring it
        LOOKUP[6][t[2]] = t[1] #if I get to this point it obviously didn't work so it is a period once more
    return ''

def checkSum(pzl):
    n = 0
    for x in pzl:
        n += int(x)
    print(n)
    return n

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
            nbrs = LOOKUP[4][x] #all neighboring indices for that period
            posSyms = set()
            for nbr in nbrs:
                posSyms.add(start[nbr]) #all characters from the SYMSET it shares a constraint with
            posSyms = LOOKUP[5] - posSyms #complement of that or all possible characters for that position
            LOOKUP[6][x] = posSyms #dictionary with period indices as keys and possible characters as values
    s = bruteForce(start)
    if s == '': print('No solution possible')
    else: print(s)
    checkSum(s)
    LOOKUP[6] = {}
    LOOKUP[7] = []

print('\nTime: ', time.time()-startTime, 's', sep='')