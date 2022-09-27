import time
import math
import sys
import random

NUM = 5

def printFormat(pzl):
    print('', pzl[8], pzl[7], pzl[14], pzl[13], pzl[9])
    print(pzl[0], pzl[1], pzl[2], pzl[6], pzl[5], pzl[15], pzl[16], pzl[12], pzl[11], pzl[10], sep='')
    print(pzl[19], pzl[3], pzl[4], pzl[17], pzl[18])

def check(pzl):
    groups = [
        [pzl[0], pzl[1], pzl[10], pzl[19]],
        [pzl[1], pzl[0], pzl[2], pzl[8]], 
        [pzl[2], pzl[1], pzl[3], pzl[6]],
        [pzl[3], pzl[2], pzl[4], pzl[19]],
        [pzl[4], pzl[3], pzl[5], pzl[17]],
        [pzl[5], pzl[4], pzl[6], pzl[15]],
        [pzl[6], pzl[2], pzl[5], pzl[7]],
        [pzl[7], pzl[6], pzl[8], pzl[14]],
        [pzl[8], pzl[1], pzl[7], pzl[9]],
        [pzl[9], pzl[8], pzl[10], pzl[13]],
        [pzl[10], pzl[0], pzl[9], pzl[11]],
        [pzl[11], pzl[10], pzl[12], pzl[18]],
        [pzl[12], pzl[11], pzl[13], pzl[16]],
        [pzl[13], pzl[9], pzl[12], pzl[14]], 
        [pzl[14], pzl[7], pzl[13], pzl[15]],
        [pzl[15], pzl[5], pzl[14], pzl[16]],
        [pzl[16], pzl[12], pzl[15], pzl[17]],
        [pzl[17], pzl[4], pzl[16], pzl[18]],
        [pzl[18], pzl[11], pzl[17], pzl[19]],
        [pzl[19], pzl[0], pzl[3], pzl[18]]
    ]
    for group in groups:
        for x in range(1, NUM+1):
            if group.count(str(x)) > 1:
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
        for x in range(1, NUM+1):
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