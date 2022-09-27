import time
import math
import sys
import random

arr = sys.argv[1:]
qB = False
if 'B' in arr:
    qB = True
    arr.pop(arr.index('B'))

def checkA(pzl):
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
    
def checkB(pzl):
    rows = [[pzl[0],  pzl[1],  pzl[2],  pzl[3],  pzl[4]],
            [pzl[5],  pzl[6],  pzl[7],  pzl[8],  pzl[9],  pzl[10], pzl[11]],
            [pzl[12], pzl[13], pzl[14], pzl[15], pzl[16], pzl[17], pzl[18]],
            [pzl[19], pzl[20], pzl[21], pzl[22], pzl[23]],
            [pzl[0],  pzl[1],  pzl[5],  pzl[6],  pzl[12]],
            [pzl[2],  pzl[3],  pzl[7],  pzl[8],  pzl[13], pzl[14], pzl[19]],
            [pzl[4],  pzl[9],  pzl[10], pzl[15], pzl[16], pzl[20], pzl[21]],
            [pzl[11], pzl[17], pzl[18], pzl[22], pzl[23]],
            [pzl[3],  pzl[4],  pzl[10], pzl[11], pzl[18]],
            [pzl[1],  pzl[2],  pzl[8],  pzl[9],  pzl[16], pzl[17], pzl[23]],
            [pzl[0],  pzl[6],  pzl[7],  pzl[14], pzl[15], pzl[21], pzl[22]],
            [pzl[5],  pzl[12], pzl[13], pzl[19], pzl[20]] ]
    for row in rows:
        for x in range(1, 8):
            if row.count(str(x)) > 1:
                return False
    return True

def isInvalid(pzl):
    excess = pzl.replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('.', '')
    if len(excess) > 0: return True
    if qB:
        return not checkB(pzl)
    else:
        return not checkA(pzl)

def isSolved(pzl):
    return '.' not in pzl
    
def bruteForce(pzl):
    if isInvalid(pzl): return ''
    if isSolved(pzl): return pzl
    
    setOfChoices = []
    if '.' in pzl:
        if qB:
            for x in range(1, 8):
                setOfChoices.append(pzl.replace('.', str(x), 1))
        else:
            for x in range(1, 7):
                setOfChoices.append(pzl.replace('.', str(x), 1))
        
    for subPzl in setOfChoices:
        bF = bruteForce(subPzl)
        if bF: return bF
    return ''

s = bruteForce(arr[0])
if s == '':
    print('No solution possible')
else:
    print(s)