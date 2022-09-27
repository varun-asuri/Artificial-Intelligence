import sys
import math
import time
import re
import random

startTime = time.time()
dictalpha, switch = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}, {'X':'O', 'O':'X'}
winnables, pzl, params, cache, moves = [], '.'*27+'OX......XO'+27*'.', ['X', set(), [], 'O'], {}, []
formatted = [d.upper() for d in sys.argv[1:]]
moveSel = {
    ('...........................OX......XO...........................', 'X') : 19,
    ('..................OX.......OX......XO...........................', 'X') : 26,
    ('..................OOO.....XXO......XO...........................', 'X') : 29,
    ('..................OOO.O...XXXO.....XO...........................', 'X') : 10,
    ('..........X......OOOO.O...XXXO.....XO...........................', 'X') : 11,
    ('..........XX.....OOXO.O..OOOOO.....XO...........................', 'X') : 34,
    ('..........XX.....OXXO.O..OXOOO...OOOO...........................', 'X') : 21,
    ('..........XXO....OXOOXO..OOOOO...OOOO...........................', 'X') : 13,
    ('..O.......OOXX...OOOOXO..OOOOO...OOOO...........................', 'X') : 16,
    ('..O.O.....OOOO..XXXXOXO..OOOOO...OOOO...........................', 'X') : 5,
    ('..O.OX....OOXX..XOXXOXO.OOOOOO...OOOO...........................', 'X') : 32,
    ('..O.OX...OOOXX..XOOXOXO.XXOOOO..XOOOO...........................', 'X') : 40,
    ('..O.OX...OOOXX..XOOXOXO.XOXOOO..XOOOO...XO......................', 'X') : 50,
    ('..O.OX...OOOOOO.XOOXOOO.XOXOOO..XOOOO...XX........X.............', 'X') : 8,
    ('..O.OX..XOOOOOO.XXOXOOO.XOXOOO..XOOOO...XO.......OX.............', 'X') : 57,
    ('..O.OOO.XOOOOOO.XXOXOOO.XXXOOO..XXOOO...XX.......XX......X......', 'X') : 3,
    ('.OOXOOO.XOOXOOO.XXOOOOO.XXXOOO..XXOOO...XX.......XX......X......', 'X') : 0,
    ('XXXXOOO.XOOXOOO.XXOOOOO.XXXOOO..XXOOO...XO......OXX......X......', 'X') : 56,
    ('XXXXOOO.XOOXOOO.XXOOOOO.XXXOOO..XXOOO...XO......XXO.....XX.O....', 'X') : 7,
    ('XXXXXXXXXOOXOOO.XXOOOOO.XXXOOO..XXOOO...XO......XXO.....XX.O....', 'X') : 15,
    ('XXXXXXXXXOOXXXXXXXOOOOO.XXXOOO..XXOOO...XO......XXO.....XX.O....', 'X') : 23,
    ('XXXXXXXXXOOXXXXXXXXXXXXXXXXOOO..XXOOO...XO......XXO.....XX.O....', 'X') : 30,
    ('XXXXXXXXXOOXXXXXXXXOXXXXXXXXOXX.XXOOOO..XO......XXO.....XX.O....', 'X') : 42,
    ('XXXXXXXXXOOXXXXXXXXOXXXXXXXOXXX.XXXOOO..XXXO....XXO.....XX.O....', 'X') : 58,
    ('XXXXXXXXXOOXXXXXXXXOXXXXXXXOOOOOXXXOOO..XXXO....XXX.....XXXO....', 'X') : 60,
    ('XXXXXXXXXOOXXXXXXXXOXXXXXXXOOOOOXXXOOO..XXXO....XXX.....XXXXX...', 'X') : 51,
    ('XXXXXXXXXOOXXXXXXXXXXXXXXXXXOOOOXXXXOO..XXXX....XXXX....XXXXX...', 'X') : 44,
    ('XXXXXXXXXOOXXXXXXXOXXXXXXXXOXOXOXXXXOO..XXXXXO..XXXX....XXXXX...', 'X') : 54,
    ('XXXXXXXXXXOXXXXXXXXXXXXXXXXXXOXOXXXXXO..XXXXXO..XXXX.OX.XXXXX...', 'X') : 61,
    ('XXXXXXXXXXOXXXXXXXXOXXXXXXXXOXXOXXXXXO..XXXXXXO.XXXX.XX.XXXXXX..', 'X') : 55,
    ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXOXXXXXX..XXXXXXX.XXXX.XXXXXXXXX..', 'X') : 39,
    ('...................X.......XX......XO...........................', 'O') : 34,
    ('...................X.......XX.....XOO....X......................', 'O') : 21,
    ('...................X.O.....XXX....XOO....X......................', 'O') : 20,
    ('...........X.......XXO.....XOX....XOO....X......................', 'O') : 37,
    ('...........X.......XXXX....XOO....XOOO...X......................', 'O') : 12,
    ('...........XXX.....XXXX....XOO....XOOO...X......................', 'O') : 26,
    ('...........XXX....XXXXX...XOOO....XOOO...X......................', 'O') : 10,
    ('..........OXXX....XOXXX...XXXXX...XOOO...X......................', 'O') : 4,
    ('....O.....OXOX....XOOXX...XXOXX...XXXXX..X......................', 'O') : 3,
    ('..XOO.....XXOX....XOXXX...XXOXX...XXXXX..X......................', 'O') : 1,
    ('.OOOOX....OXXX....XXXXX...XXOXX...XXXXX..X......................', 'O') : 6,
    ('.OOOOOO..XXXXX....XXXXX...XXOXX...XXXXX..X......................', 'O') : 25,
    ('.OOOOOO..XXOXX...XXXXXX..OXOOXX...XXXXX..X......................', 'O') : 0,
    ('OOOOOOO..OXOXX...XOXXXX..XXOOXX..XXXXXX..X......................', 'O') : 40,
    ('OOOOOOO..OXOOX...XOOXXX..XOOOXX.XXXXXXX.OX......................', 'O') : 8,
    ('OOOOOOO.OOXOOX..XXXXXXX..XOOOXX.XXXXXXX.OX......................', 'O') : 24,
    ('OOOOOOO.OOOOOX..OOXXXXX.OOOOOXX.OXXXXXX.OX......................', 'O') : 49,
    ('OOOOOOO.OOOOOX..OOXXXXX.OOOOOXX.OOXXXXX.OX......XO..............', 'O') : 56,
    ('OOOOOOO.OOOOOX..OOXXXXX.OOOOOXX.OOXXXXX.OX......OX......OX......', 'O') : 58,
    ('OOOOOOO.OOOOOX..OOXXXXX.OOOOOXX.OOXXXXX.OX......OO......OOO.....', 'O') : 50,
    ('OOOOOOO.OOOOOX..OOXXXXX.OOOOOXX.OOXXXXX.OO......OOO.....OOO.....', 'O') : 42,
    ('OOOOOOO.OOOOOX..OOXXXXX.OOOXOXX.OOOXXXX.OOOX....OOO.....OOO.....', 'O') : 51,
    ('OOOOOOO.OOOOOX..OOXOXXX.OOOOOXX.OOOOXXX.OOOO....OOOO....OOO.....', 'O') : 14,
    ('OOOOOOO.OOOOOOO.OOXOXOX.OOOOOXX.OOOOXXX.OOOO....OOOO....OOO.....', 'O') : 23,
    ('OOOOOOO.OOOOOOOXOOXOXOXOOOOOOXX.OOOOXXX.OOOO....OOOO....OOO.....', 'O') : 7,
    ('OOOOOOOOOOOOOOOOOOXOXOXOOOOOOXX.OOOOXXX.OOOO....OOOO....OOO.....', 'O') : 47,
    ('OOOOOOOOOOOOOOOOOOXOOOXOOOOOOOX.OOOOXXX.OOOO..XOOOOO....OOO.....', 'O') : 31,
    ('OOOOOOOOOOOOOOOOOOXOOOOOOOOOOOOOOOOOXXX.OOOO..XOOOOO....OOO.....', 'O') : 39,
    ('OOOOOOOOOOOOOOOOOOXOOOOOOOOXOOOOOOOOXOOOOOOO.XXOOOOO....OOO.....', 'O') : 54}
cre = [re.compile('XO+$'), re.compile('^O+X'), re.compile('OX+$'), re.compile('^X+O')]
given, corners = False, {0, 7, 56, 63}
weights = [
     99,-15, 5, 4, 4, 5,-15, 99,
    -15,-20, 4, 1, 1, 4,-20,-15,
      5,  4, 3, 2, 2, 3,  4,  5,
      4,  1, 2, 0, 0, 2,  1,  5,
      4,  1, 2, 0, 0, 2,  1,  4,
      5,  4, 3, 2, 2, 3,  4,  5,
    -15,-20, 4, 1, 1, 4,-20,-15,
     99,-15, 5, 4, 4, 5,-15, 99]
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

def flipVertical(pzl):
    newPzl = ''
    for n in range(8):
        row = pzl[n*8: (n+1)*8]
        newPzl += row[::-1]
    return newPzl
def flipHorizontal(pzl):
    newPzl = ''
    for n in range(8):
        row = pzl[n*8: (n+1)*8]
        newPzl = row + newPzl
    return newPzl
def transpose(pzl):
    newPzl = ''
    for n in range(8):
        col = pzl[n:len(pzl):8]
        newPzl += col
    return newPzl
def calculatePosition(x, degree):
    if degree == 90: return 56-8*(x%8)+(x//8)
    elif degree == 180: return 63-x
    else: return 7+8*(x%8)-(x//8)
def setGlobals():
    for n in range(64):
        row = list(range(n//8*8, (n//8+1)*8))
        if len(row) >= 3 and row not in winnables: winnables.append(row)
        column = list(range(n%8, 64, 8))
        if len(column) >= 3 and column not in winnables: winnables.append(column)
        if not n%8 in [0,8-1] or n//8 in [0, 8]:
            forward = []
            for x in range(n,64,8+1):
                forward.append(x)
                if not (x+1)%8: break
            for x in range(n-8-1,-1,-8-1):
                if not (x+1)%8: break
                forward.append(x)
            forward.sort()
            if len(forward) >= 3 and forward not in winnables: winnables.append(forward)
            backward = []
            for x in range(n,64,8-1):
                backward.append(x)
                if not x%8: break
            for x in range(n-8+1,-1,-8+1):
                if not x%8: break
                backward.append(x)
            backward.sort()
            if len(backward) >= 3 and backward not in winnables: winnables.append(backward)
def printFormat(pzl):
    for n in range(8): print(pzl[n*8:(n+1)*8])
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
def securePiece(board, indx, piece):
    row = indx%8
    col = indx//8
    topLeft = True
    topRight = True
    bottomLeft = True
    bottomRight = True
    for a in range(row+1):
        for b in range(col+1):
            if board[b*8+a] != piece: topLeft = False
    for a in range(row, 8):
        for b in range(col, 8):
            if board[b*8+a] != piece: bottomRight = False
    for a in range(row+1):
        for b in range(col, 8):
            if board[b*8+a] != piece: bottomLeft = False
    for a in range(row, 8):
        for b in range(col+1):
            if board[b*8+a] != piece: topRight = False
    return topLeft or topRight or bottomLeft or bottomRight
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
def alphaBeta(brd, token, lower, upper):
    poss = genPossible(brd, token)
    poss2 = genPossible(brd, switch[token])
    score = brd.count(token) - brd.count(switch[token])
    if not poss:
        if not poss2: return [score]
        result = alphaBeta(brd, switch[token], -upper, -lower)
        return [-result[0]] + result[1:] + [-1]
    best = [lower-1]
    for move in poss:
        nm = alphaBeta(placeChar(move, brd, token), switch[token], -upper, -lower)
        score = -nm[0]
        if score > upper: return [score]
        if score < lower: continue
        best = [score] + nm[1:] + [move]
        lower = score + 1
    return best
def heuristicMove(board, token):
    a = board.count(token)
    b = board.count(switch[token])
    n = 0
    for c in corners: 
        if board[c] == params[0]: n += 100
        elif board[c] == params[1]: n -= 100
    p = genPossible(board, switch[token])
    p2 = genPossible(board, token)
    n += (100/(3**len(p)))
    if not p and not p2: n += a-b * 250
    if board[0] == switch[token]:
        weights[2:4] = [-4, -2]
        weights[16:25:8] = [-4, -2]
    if board[7] == switch[token]:
        weights[4:6] = [-2, -4]
        weights[22:31:8] = [-4, -2]
    if board[56] == switch[token]:
        weights[32:41:8] = [-2, -4]
        weights[58:60] = [-4, -2]
    if board[63] == switch[token]:
        weights[40:49:8] = [-2, -4]
        weights[60:62] = [-2, -4]
    if board[0] == token:
        weights[1:4] = [7, 5, 3]
        weights[8:25:8] = [7, 5, 3]
        weights[9] = 5
    if board[7] == token:
        weights[4:7] = [3, 5, 7]
        weights[14:31:8] = [7, 5, 3]
        weights[14] = 5
    if board[56] == token:
        weights[32:49:8] = [3, 5, 7]
        weights[57:60] = [7, 5, 3]
        weights[49] = 5
    if board[63] == token:
        weights[40:57:8] = [3, 5, 7]
        weights[60:63] = [3, 5, 7]
        weights[54] = 5
    for num in range(64):
        if board[num] == token:
            if securePiece(board, num, token): n += 15
            else: n += weights[num]
        elif board[num] == switch[token]:
            if securePiece(board, num, switch[token]): n -= 15
            else: n -= weights[num]
    for m in p:
        if m in corners: n -= 100
    for m in p2:
        if m in corners: n += 20
    return n
def midGame(brd, token, indx, level, player):
    poss = genPossible(brd, token)
    poss2 = genPossible(brd, switch[token])
    score = heuristicMove(brd, player)
    if level == 0: return score, indx
    if not poss:
        if not poss2: return score, indx
        token = switch[token]
        indx = [-1] + indx
        poss, poss2 = poss2, poss
    nmList = [midGame(placeChar(new_indx, brd, token), switch[token], [new_indx] + indx, level-1, player) for new_indx in poss]
    if token == player: return max(nmList)
    else: return min(nmList)

setGlobals()
params[1] = genPossible(pzl, params[0])
if not len(params[1]):
    params[0], params[3] = params[3], params[0]
    params[1] = genPossible(pzl, params[0])
if params[1]:
    period = pzl.count('.')
    pzl90, pzl180, pzl270 = flipVertical(transpose(pzl)), pzl[::-1], flipHorizontal(transpose(pzl))
    if (pzl, params[0]) in moveSel: final = [moveSel[(pzl, params[0])]]
    elif (pzl90, params[0]) in moveSel: final = [calculatePosition(moveSel[(pzl90, params[0])], 90)]
    elif (pzl180, params[0]) in moveSel: final = [calculatePosition(moveSel[(pzl180, params[0])], 180)]
    elif (pzl270, params[0]) in moveSel: final = [calculatePosition(moveSel[(pzl270, params[0])], 270)]
    elif period > 9: final = max([(heuristicMove(placeChar(x, pzl, params[0]), params[0]), x) for x in list(params[1])])
    else: final = alphaBeta(pzl, params[0], -64, 64)
print(final[-1])