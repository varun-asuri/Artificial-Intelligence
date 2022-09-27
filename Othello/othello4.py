import sys
import math
import time
import re
import random

startTime = time.time()
dictalpha, switch = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}, {'X':'O', 'O':'X'}
winnables, invals, pzl, params, cache, moves = [], (64, 8, 8), '.'*27+'OX......XO'+27*'.', ['X', set(), [], 'O'], {}, []
formatted = [d.upper() for d in sys.argv[1:]]
cre = [re.compile('XO+$'), re.compile('^O+X'), re.compile('OX+$'), re.compile('^X+O')]
given, corners = False, {0, 7, 56, 63}
weights = [
    10, -5, 3, 4, 4, 3, -5, 10,
    -5, -7, 3, 1, 1, 3, -7, -5,
     3,  3, 4, 2, 2, 4,  3,  3,
     4,  1, 2, 1, 1, 2,  1,  4,
     4,  1, 2, 1, 1, 2,  1,  4,
     4,  3, 4, 2, 2, 4,  3,  3,
    -5, -7, 3, 1, 1, 3, -7, -5,
    10, -5, 3, 4, 4, 3, -5, 10]
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
        if y >= 0: params[2].append(int(n))
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
def printFormat(pzl, invals):
    for n in range(invals[2]): print(pzl[n*invals[1]:(n+1)*invals[1]])
def genPossible(pzl, sym):
    if (pzl, sym) in cache: return cache[(pzl, sym)]
    returnable = set()
    for const in winnables:
        cut = pzl[const[0]:const[-1]+1:const[1]-const[0]]
        indx = 0
        while '.' in cut:
            new_i = cut.find('.')
            indx += new_i
            before, after = cut[:new_i], cut[new_i+1:]
            if sym == 'X':
                if cre[0].search(before) or cre[1].search(after): returnable.add(const[indx])
            else:
                if cre[2].search(before) or cre[3].search(after): returnable.add(const[indx])
            indx += 1
            cut = after
    cache[(pzl, sym)] = returnable
    return returnable
def placeChar(indx, board, sym):
    if (indx, board, sym) in cache: return cache[(indx, board, sym)]
    newPzl = board
    care, strs = [], []
    for w in winnables:
        if indx in w:
            care.append(w)
            strs.append(board[w[0]:w[-1]+1:w[1]-w[0]])
    factor = 0
    for i, s in enumerate(strs[:]):
        if switch[sym] not in s or sym not in s:
            care.pop(i-factor)
            factor += 1
    for a in care:
        minor_i = a.index(indx)
        before, after = a[:minor_i][::-1], a[minor_i+1:]
        if len(before) > 1:
            if before[-1] == 0: before_s = board[before[0]::before[1]-before[0]]
            else: before_s = board[before[0]:before[-1]-1:before[1]-before[0]]
        elif len(before): before_s = board[before[0]]
        else: before_s = ''
        if len(after) > 1: after_s = board[after[0]:after[-1]+1:after[1]-after[0]]
        elif len(after): after_s = board[after[0]]
        else: after_s = ''
        if switch[sym] == 'O':
            bx = cre[1].search(before_s)
            if bx:
                xpoint = bx.span()[1] - 1
                for f in range(xpoint): newPzl = newPzl[:before[f]] + sym + newPzl[before[f]+1:]
            ax = cre[1].search(after_s)
            if ax:
                xpoint = ax.span()[1] - 1
                for f in range(xpoint): newPzl = newPzl[:after[f]] + sym + newPzl[after[f]+1:]
        else:
            bo = cre[3].search(before_s)
            if bo:
                opoint = bo.span()[1] - 1
                for f in range(opoint): newPzl = newPzl[:before[f]] + sym + newPzl[before[f]+1:]
            ao = cre[3].search(after_s)
            if ao:
                opoint = ao.span()[1] - 1
                for f in range(opoint): newPzl = newPzl[:after[f]] + sym + newPzl[after[f]+1:]
    newPzl = newPzl[:indx] + sym + newPzl[indx+1:]
    cache[(indx, board, sym)] = newPzl
    return newPzl
def heuristicMove(pzl, board, indx):
    a = (board.count(params[0])-pzl.count(params[0]))/100
    n = 0
    p = genPossible(board, params[1])
    if not p: n += 10
    n += weights[indx]
    if indx in {1, 8, 9} and board[0] == params[0]: n += 6
    if indx in {6, 14, 15} and board[7] == params[0]: n += 6
    if indx in {48, 49, 57} and board[56] == params[0]: n += 6
    if indx in {54, 55, 63} and board[63] == params[0]: n += 6
    for sample in corners:
        for w in winnables:
            if sample in w and indx in w:
                if indx < sample: sect = board[indx:sample+1:w[1]-w[0]]
                else: sect = board[sample:indx+1:w[1]-w[0]]
                if not sect.replace(params[0], ''): n += 2.5
    if p & corners: n -= 20
    n += math.floor(len(p) * -1)
    return n + a

setGlobals(invals)
params[1] = genPossible(pzl, params[0])
if not len(params[1]):
    params[0], params[3] = params[3], params[0]
    params[1] = genPossible(pzl, params[0])
if params[1]:
    period = pzl.count('.')
    answer = []
    for x in list(params[1]):
        newPzl = placeChar(x, pzl, params[0])
        wins = heuristicMove(pzl, newPzl, x)
        answer.append( (wins, x, newPzl) )
    final = max(answer)
    print(final[1])