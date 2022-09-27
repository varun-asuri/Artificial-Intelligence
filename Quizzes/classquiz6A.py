import time
import math
import sys
import random

def printFormat(pzl):
    print(' ' + pzl[:5])
    print(pzl[5:12])
    print(pzl[12:19])
    print(' ' + pzl[19:])

def check(pzl):
    hexagons = [[pzl[0],  pzl[1],  pzl[2],  pzl[6],  pzl[7],  pzl[8] ],
                [pzl[2],  pzl[3],  pzl[4],  pzl[8],  pzl[9],  pzl[10]],
                [pzl[5],  pzl[6],  pzl[7],  pzl[12], pzl[13], pzl[14]],
                [pzl[7],  pzl[8],  pzl[9],  pzl[14], pzl[15], pzl[16]],
                [pzl[9],  pzl[10], pzl[11], pzl[16], pzl[17], pzl[18]],
                [pzl[13], pzl[14], pzl[15], pzl[19], pzl[20], pzl[21]],
                [pzl[15], pzl[16], pzl[17], pzl[21], pzl[22], pzl[23]]]
    for hexagon in hexagons:
        for x in range(1, 7):
            if hexagon.count(str(x)) > 1:
                return False
    
    return True

def isInvalid(pzl):
    excess = pzl.replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('.', '')
    if len(excess) > 0: return True
    return not check(pzl)

def isSolved(pzl):
    return '.' not in pzl
    
def bruteForce(pzl):
    if isInvalid(pzl): return ''
    if isSolved(pzl): return pzl
    
    setOfChoices = []
    if '.' in pzl:
        for x in range(1, 7):
            setOfChoices.append(pzl.replace('.', str(x), 1))
        
    for subPzl in setOfChoices:
        bF = bruteForce(subPzl)
        if bF: return bF
    return ''

s = bruteForce(sys.argv[1])
s = s.replace('1', 'A')
s = s.replace('2', 'B')
s = s.replace('3', 'C')
s = s.replace('4', 'D')
s = s.replace('5', 'E')
s = s.replace('6', 'F')
print(s)
printFormat(s)
print(s.count('A'), s.count('B'), s.count('C'), s.count('D'), s.count('E'), s.count('F'))