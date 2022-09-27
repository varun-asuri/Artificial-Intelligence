import sys
import math
import time
import re

startTime = time.time()
winnables, invals, pzl, params = [], (64, 8, 8), '.'*27+'OX......XO'+27*'.', ['X', set()]
formatted = [d.upper() for d in sys.argv[1:]]
given = False
for n in formatted:
    if len(n) == 64: pzl = n
    elif n in ['X','O']:
        given = True
        params[0] = n
    else: params[2].append(int(n))
if not given:
    if pzl.count('.')%2: params[0] = 'O'
    else: params[0] = 'X'

def setGlobals(invals):
    for n in range(invals[0]):
        row = list(range(n//invals[2]*invals[2], (n//invals[2]+1)*invals[2]))
        if len(row) >= 3 and row not in winnables: winnables.append(row)
        column = list(range(n%invals[2], invals[0], invals[2]))
        if len(column) >= 3 and column not in winnables: winnables.append(column)
        if not n%invals[2] in [0,invals[2]-1] or n//invals[2] in [0, invals[1]]:
            forward = []
            for x in range(n,invals[0],invals[2]+1):
                forward.append(x)
                if not (x+1)%invals[2]: break
            for x in range(n-invals[2]-1,-1,-invals[2]-1):
                if not (x+1)%invals[2]: break
                forward.append(x)
            forward.sort()
            if len(forward) >= 3 and forward not in winnables: winnables.append(forward)
            backward = []
            for x in range(n,invals[0],invals[2]-1):
                backward.append(x)
                if not x%invals[2]: break
            for x in range(n-invals[2]+1,-1,-invals[2]+1):
                if not x%invals[2]: break
                backward.append(x)
            backward.sort()
            if len(backward) >= 3 and backward not in winnables: winnables.append(backward)

def genPossible(pzl):
    for n in winnables:
        s = ''.join([pzl[x] for x in n])
        cut = s[:]
        indx = 0
        while '.' in cut:
            i = cut.find('.')
            indx += i
            before, after = cut[:i], cut[i+1:]
            if params[0] == 'X':
                if re.search('x+o+$', before, re.I) or re.search('^o+x+', after, re.I):
                    params[1].add(n[indx])
            else:
                if re.search('o+x+$', before, re.I) or re.search('^x+o+', after, re.I):
                    params[1].add(n[indx])
            indx += 1
            cut = after

setGlobals(invals)
genPossible(pzl)
if not len(params[1]): print('No moves possible')
else: print(params[1])