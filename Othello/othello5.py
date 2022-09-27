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
def negaMax(brd, token, indx, level):
    if brd in cache: return (cache[brd], indx)
    poss = genPossible(brd, token)
    poss2 = genPossible(brd, switch[token])
    score = brd.count(params[0]) - brd.count(params[3])
    if not poss:
        if not poss2:
            cache[brd] = score
            return score, indx
        token = switch[token]
        indx = ['-1'] + indx
        poss, poss2 = poss2, poss
    best = ()
    curr = -65
    nmList = []
    for new_indx in poss:
        nm = negaMax(placeChar(new_indx, brd, token), switch[token], [str(new_indx)] + indx, level+1)
        nmList.append(nm)
        if int(nm[0]) > curr and level == 0:
            curr = int(nm[0])
            best = nm
            print('Score: ', nm[0], ', Reverse Move Sequence: ', ", ".join(nm[1]), sep='')
            print('Time:', time.time()-startTime)
    if token == params[0]: best = max(nmList)
    else: best = min(nmList)
    return best
def heuristicMove(pzl, board, indx):
    a = board.count(params[0])
    n = 0
    p = genPossible(board, params[3])
    if not p: n += 10
    if indx in corners: n += 10
    if p & corners: n -= 10
    n += math.floor((2.5 - len(p)) * 2)
    return n + (a-pzl.count(params[0]))

setGlobals(invals)
params[1] = genPossible(pzl, params[0])
if not len(params[1]):
    params[0], params[3] = params[3], params[0]
    params[1] = genPossible(pzl, params[0])
print('\nPossible Moves:', list(params[1]))
if params[1]:
    period = pzl.count('.')
    if period > 11:
        answer = []
        for x in list(params[1]):
            newPzl = placeChar(x, pzl, params[0])
            wins = heuristicMove(pzl, newPzl, x)
            answer.append( (wins, x, newPzl) )
        final = max(answer)
        print('Score: ', final[2].count(params[0])-final[2].count(params[3]), ', Reverse Move Sequence: ', [str(final[1])], sep='')
        print('Time:', time.time()-startTime)
    else: negaMax(pzl, params[0], [], 0)