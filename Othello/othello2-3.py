import sys
import math
import time
import re

startTime = time.time()
dictalpha = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
winnables, invals, pzl, params = [], (64, 8, 8), '.'*27+'OX......XO'+27*'.', ['X', set(), [], 'O']
formatted = [d.upper() for d in sys.argv[1:]]
given = False
for n in formatted:
    if len(n) == 64: pzl = n
    elif n in ['X','O']:
        given = True
        params[0] = n
    elif re.search('^[A-H][1-8]$', n):
        u = dictalpha[n[0]] + (int(n[1])-1)*8
        params[2].append(u)
    else:
        y = int(n)
        if y >= 0:
            params[2].append(int(n))
if not given:
    if pzl.count('.')%2: params[0] = 'O'
    else: params[0] = 'X'
if params[0] == 'X': params[3] = 'O'
else: params[3] = 'X'

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

def placeChar(indx):
    global pzl
    care, strs = [], []
    for w in winnables:
        if indx in w:
            care.append(w)
            strs.append(''.join([pzl[i] for i in w]))
    factor = 0
    for i, s in enumerate(strs[:]):
        if params[3] not in s or params[0] not in s:
            care.pop(i-factor)
            factor += 1
    for a in care:
        minor_i = a.index(indx)
        before, after = a[:minor_i][::-1], a[minor_i+1:]
        before_s, after_s = ''.join([pzl[j] for j in before]), ''.join([pzl[j] for j in after])
        if params[3] == 'O':
            if re.search('^o+x+', before_s, re.I):
                xpoint = before_s.find('X')
                for f in range(xpoint):
                    pzl = pzl[:before[f]] + params[0] + pzl[before[f]+1:]
            if re.search('^o+x+', after_s, re.I):
                xpoint = after_s.find('X')
                for f in range(xpoint):
                    pzl = pzl[:after[f]] + params[0] + pzl[after[f]+1:]
        else:
            if re.search('^x+o+', before_s, re.I):
                opoint = before_s.find('O')
                for f in range(opoint):
                    pzl = pzl[:before[f]] + params[0] + pzl[before[f]+1:]
            if re.search('^x+o+', after_s, re.I):
                opoint = after_s.find('O')
                for f in range(opoint):
                    pzl = pzl[:after[f]] + params[0] + pzl[after[f]+1:]
    pzl = pzl[:indx] + params[0] + pzl[indx+1:]

setGlobals(invals)
for c in params[2]:
    genPossible(pzl)
    if not len(params[1]): 
        params[1] = set()
        params[0], params[3] = params[3], params[0]
        genPossible(pzl)
    params[1] = sorted([str(x) for x in [*params[1]]])
    newPzl = pzl
    for i in params[1]: newPzl = newPzl[:int(i)] + '*' + newPzl[int(i)+1:]
    for n in range(invals[1]): print(newPzl[n*invals[2]:(n+1)*invals[2]])
    print('\n', pzl, ' ', pzl.count('X'), '/', pzl.count('O'), sep='')
    print('POSSIBLE MOVES FOR ', params[0], ': ', ', '.join(params[1]), sep='', end='\n\n')
    placeChar(c)
    print(params[0], 'plays to', c)
    params[0], params[3] = params[3], params[0]
    params[1] = set()
genPossible(pzl)
if not len(params[1]): 
    params[1] = set()
    params[0], params[3] = params[3], params[0]
    genPossible(pzl)
params[1] = sorted([str(x) for x in [*params[1]]])
newPzl = pzl
for i in params[1]: newPzl = newPzl[:int(i)] + '*' + newPzl[int(i)+1:]
for n in range(invals[1]): print(newPzl[n*invals[2]:(n+1)*invals[2]])
print('\n', pzl, ' ', pzl.count('X'), '/', pzl.count('O'), sep='')
print('POSSIBLE MOVES FOR ', params[0], ': ', ', '.join(params[1]), sep='', end='\n\n')
print('TOTAL TIME: ', time.time()-startTime, 's', sep='')