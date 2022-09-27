import time
import re
import math
import random

cache, corners, switch, cre = {}, {0, 7, 56, 63}, {'@':'o', 'o':'@'}, [re.compile('@o+$'), re.compile('^o+@'), re.compile('o@+$'), re.compile('^@+o')]
moveSel = {
    ('...........................o@......@o...........................', '@') : 37,
    ('..................o@.......o@......@o...........................', '@') : 26,
    ('..................ooo.....@@o......@o...........................', '@') : 29,
    ('..................ooo.o...@@@o.....@o...........................', '@') : 10,
    ('..........@......oooo.o...@@@o.....@o...........................', '@') : 11,
    ('..........@@.....oo@o.o..ooooo.....@o...........................', '@') : 34,
    ('..........@@.....o@@o.o..o@ooo...oooo...........................', '@') : 21,
    ('..........@@o....o@oo@o..ooooo...oooo...........................', '@') : 13,
    ('..o.......oo@@...oooo@o..ooooo...oooo...........................', '@') : 16,
    ('..o.o.....oooo..@@@@o@o..ooooo...oooo...........................', '@') : 5,
    ('..o.o@....oo@@..@o@@o@o.oooooo...oooo...........................', '@') : 32,
    ('..o.o@...ooo@@..@oo@o@o.@@oooo..@oooo...........................', '@') : 40,
    ('..o.o@...ooo@@..@oo@o@o.@o@ooo..@oooo...@o......................', '@') : 50,
    ('..o.o@...oooooo.@oo@ooo.@o@ooo..@oooo...@@........@.............', '@') : 8,
    ('..o.o@..@oooooo.@@o@ooo.@o@ooo..@oooo...@o.......o@.............', '@') : 57,
    ('..o.ooo.@oooooo.@@o@ooo.@@@ooo..@@ooo...@@.......@@......@......', '@') : 3,
    ('.oo@ooo.@oo@ooo.@@ooooo.@@@ooo..@@ooo...@@.......@@......@......', '@') : 0,
    ('@@@@ooo.@oo@ooo.@@ooooo.@@@ooo..@@ooo...@o......o@@......@......', '@') : 56,
    ('@@@@ooo.@oo@ooo.@@ooooo.@@@ooo..@@ooo...@o......@@o.....@@.o....', '@') : 7,
    ('@@@@@@@@@oo@ooo.@@ooooo.@@@ooo..@@ooo...@o......@@o.....@@.o....', '@') : 15,
    ('@@@@@@@@@oo@@@@@@@ooooo.@@@ooo..@@ooo...@o......@@o.....@@.o....', '@') : 23,
    ('@@@@@@@@@oo@@@@@@@@@@@@@@@@ooo..@@ooo...@o......@@o.....@@.o....', '@') : 30,
    ('@@@@@@@@@oo@@@@@@@@o@@@@@@@@o@@.@@oooo..@o......@@o.....@@.o....', '@') : 42,
    ('@@@@@@@@@oo@@@@@@@@o@@@@@@@o@@@.@@@ooo..@@@o....@@o.....@@.o....', '@') : 58,
    ('@@@@@@@@@oo@@@@@@@@o@@@@@@@ooooo@@@ooo..@@@o....@@@.....@@@o....', '@') : 60,
    ('@@@@@@@@@oo@@@@@@@@o@@@@@@@ooooo@@@ooo..@@@o....@@@.....@@@@@...', '@') : 51,
    ('@@@@@@@@@oo@@@@@@@@@@@@@@@@@oooo@@@@oo..@@@@....@@@@....@@@@@...', '@') : 44,
    ('@@@@@@@@@oo@@@@@@@o@@@@@@@@o@o@o@@@@oo..@@@@@o..@@@@....@@@@@...', '@') : 54,
    ('@@@@@@@@@@o@@@@@@@@@@@@@@@@@@o@o@@@@@o..@@@@@o..@@@@.o@.@@@@@...', '@') : 61,
    ('@@@@@@@@@@o@@@@@@@@o@@@@@@@@o@@o@@@@@o..@@@@@@o.@@@@.@@.@@@@@@..', '@') : 55,
    ('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@o@@@@@@..@@@@@@@.@@@@.@@@@@@@@@..', '@') : 39,
    ('...................@.......@@......@o...........................', 'o') : 34,
    ('...................@.......@@.....@oo....@......................', 'o') : 21,
    ('...................@.o.....@@@....@oo....@......................', 'o') : 20,
    ('...........@.......@@o.....@o@....@oo....@......................', 'o') : 37,
    ('...........@.......@@@@....@oo....@ooo...@......................', 'o') : 12,
    ('...........@@@.....@@@@....@oo....@ooo...@......................', 'o') : 26,
    ('...........@@@....@@@@@...@ooo....@ooo...@......................', 'o') : 10,
    ('..........o@@@....@o@@@...@@@@@...@ooo...@......................', 'o') : 4,
    ('....o.....o@o@....@oo@@...@@o@@...@@@@@..@......................', 'o') : 3,
    ('..@oo.....@@o@....@o@@@...@@o@@...@@@@@..@......................', 'o') : 1,
    ('.oooo@....o@@@....@@@@@...@@o@@...@@@@@..@......................', 'o') : 6,
    ('.oooooo..@@@@@....@@@@@...@@o@@...@@@@@..@......................', 'o') : 25,
    ('.oooooo..@@o@@...@@@@@@..o@oo@@...@@@@@..@......................', 'o') : 0,
    ('ooooooo..o@o@@...@o@@@@..@@oo@@..@@@@@@..@......................', 'o') : 40,
    ('ooooooo..o@oo@...@oo@@@..@ooo@@.@@@@@@@.o@......................', 'o') : 8,
    ('ooooooo.oo@oo@..@@@@@@@..@ooo@@.@@@@@@@.o@......................', 'o') : 24,
    ('ooooooo.ooooo@..oo@@@@@.ooooo@@.o@@@@@@.o@......................', 'o') : 49,
    ('ooooooo.ooooo@..oo@@@@@.ooooo@@.oo@@@@@.o@......@o..............', 'o') : 56,
    ('ooooooo.ooooo@..oo@@@@@.ooooo@@.oo@@@@@.o@......o@......o@......', 'o') : 58,
    ('ooooooo.ooooo@..oo@@@@@.ooooo@@.oo@@@@@.o@......oo......ooo.....', 'o') : 50,
    ('ooooooo.ooooo@..oo@@@@@.ooooo@@.oo@@@@@.oo......ooo.....ooo.....', 'o') : 42,
    ('ooooooo.ooooo@..oo@@@@@.ooo@o@@.ooo@@@@.ooo@....ooo.....ooo.....', 'o') : 51,
    ('ooooooo.ooooo@..oo@o@@@.ooooo@@.oooo@@@.oooo....oooo....ooo.....', 'o') : 14,
    ('ooooooo.ooooooo.oo@o@o@.ooooo@@.oooo@@@.oooo....oooo....ooo.....', 'o') : 23,
    ('ooooooo.ooooooo@oo@o@o@oooooo@@.oooo@@@.oooo....oooo....ooo.....', 'o') : 7,
    ('oooooooooooooooooo@o@o@oooooo@@.oooo@@@.oooo....oooo....ooo.....', 'o') : 47,
    ('oooooooooooooooooo@ooo@ooooooo@.oooo@@@.oooo..@ooooo....ooo.....', 'o') : 31,
    ('oooooooooooooooooo@ooooooooooooooooo@@@.oooo..@ooooo....ooo.....', 'o') : 39,
    ('oooooooooooooooooo@oooooooo@oooooooo@ooooooo.@@ooooo....ooo.....', 'o') : 54,
    ('...........................o@......@@@...ooo....................', '@') : 18,
    ('..................@........@@o.....@o@...ooo....................', '@') : 45,
    ('..................@.......oooo.....@@@...ooo.@..................', '@') : 21,
    ('..........o.......o..@....oo@@.....@@@...ooo.@..................', '@') : 50,
    ('..........o.......o..@....oo@@.....o@@..@@@o@@....@o............', '@') : 60,
    ('..........o.......oo.@....ooo@.@...ooo@.@@@@@@@@..@@.@......@@..', '@') : 11,
    ('..@.......@@......@@.@....@@o@.@.ooooo@.@@@@@@@@..@@.@......@@..', '@') : 32,
    ('....................o....o.oo.....o@o@.....o@@.......@..........', '@') : 12,
    ('............@o......o....o.o@.....o@@@.....o@@.......@..........', '@') : 42,
    ('....o.......oo......o....o@o@.....o@@@...o@@@@.......@..........', '@') : 40,
    ('....o.......oo....o.o....ooo@.....o@@@..@@@@@@.......@..........', '@') : 10,
    ('..o.o.....oooo....o@o...@o@@@...o.@@@@..@@@@@@.......@..........', '@') : 3,
    ('..ooooo...o@@o..o.o@o...oo@@@...o.@@@@..@@@@@@.......@..........', '@') : 21,
    ('.....................@.....o@o....oooo......@o..................', '@') : 53,
    ('.....................@@@...o@o....ooooo.....@@.......@..........', '@') : 30,
    ('.....................@@@...ooo@@..ooo@o@....@@.o.....@..........', '@') : 26,
    ('..................o..@@@..oo@@@@..o@o@o@....@@.o.....@..........', '@') : 17,
    ('................ooo..@@@..@o@@@@..o@o@o@....@@.o.....@..........', '@') : 10,
    ('..@@@.....@.....oo@..@@@.ooo@@@@..ooo@o@...o@@.o.....@..........', '@') : 42,
    ('..@@@.....@.....oo@..@@@.o@o@@@@..o@o@o@.o@@@@.o.....@..........', '@') : 40,
    ('..@@@.....@.....o@oo.@@@oo@o@@@@o.o@o@o@@@@@@@.o.....@..........', '@') : 11,
    ('..@@@.....@@....o@o@.@@@oo@@@@@@o.o@o@o@oo@@@@.oo....@..........', '@') : 33,
    ('..@@@.....@@....o@o@.@@@o@@@@@@@oo@@o@o@ooo@@@.oo..o.@..........', '@') : 59,
    ('..@@@.....@@....o@o@.@@@o@@@@@@@oo@@o@o@ooo@@@.oo..o.@.....@o...', '@') : 50,
    ('..........o.....oooo@@@@oo.@o@o@o@@@@o@@o@@o@@@@.@@@o@....ooooo.', '@') : 11,
    ('.....................@@@..oo@@@...oo@@@@..@o@@@....oo@....@@@o..', '@') : 62,
    ('.@@@@@.....@o@@o..@@@@oo.o.@@oooo.o@oooo@@@o@@oo..ooo@....ooooo.', '@') : 24,
    ('.....................@.....o@@@....oo......o@...................', 'o') : 45,
    ('..o..@.....o.@......o@..o.ooo@@oo..oo@.ooooo@@oo..@@.@..........', 'o') : 58,
    ('..o..@.....o.@....@.o@..o.o@o@@oo@.o@@.ooo@o@@oo..o@.@....oooo..', 'o') : 38,
    ('..o.@@.....@.@....@.o@..o.o@oo@oo@.ooooooo@o@@oo..o@.@....oooo..', 'o') : 10,
    ('..o.@@....o@.@..ooo@@@..o.@@oo@oo@.@oooooo@o@@oo..o@.@....oooo..', 'o') : 3,
    ('.@@@@@....oo.@..oooo@@..oooooo@ooooooooooo@o@@oo..o@.@....oooo..', 'o') : 52,
    ('...o......@.oo....@..o....@ooooo...@oo.o...o@o.o.....@..........', 'o') : 42,
    ('...o......@.oo....@..o.@..@ooo@o...oo@.o..oo@o.o.....@..........', 'o') : 61,
    ('...o......@.oo....@..o.@..@ooo@o...oo@.o..oo@@@o.....o.......o..', 'o') : 17,
    ('..@o......@.oo...o@..o.@..oooo@o...oo@.o..oo@@@o.....o.......o..', 'o') : 19,
    ('..@@@.....@.o@..oooo.o@@o.oooo@@o..oooo@..oo@@@@.....@.@...ooo..', 'o') : 52,
    ('.ooooo....o@@o..ooo@@@@@o.@oo@@@o@.ooo@@..oooo@@....o@.@...ooo..', 'o') : 40,
    ('.ooooo....o@oo..oooo@@@@o.ooo@@@oo.o@o@@o.o@oo@@..@.o@.@...ooo..', 'o') : 58,
    ('.ooooo....o@oo..oooo@@@@o.ooo@@@oo.o@o@@o@@@oo@@..o.o@.@..oooo..', 'o') : 51,
    ('................o.ooo@..o..o@...o@o@o@....@..@.......@..........', 'o') : 22,
    ('...........@....o.o@ooo.o..@@...o@o@o@....@..@.......@..........', 'o') : 2,
    ('..ooo......o....o.o@ooo.o..@@...o@@@o@...@@..@.......@..........', 'o') : 43,
    ('..ooo......o....o.ooooo.o..o@...o@@oo@...@@@.@......@@..........', 'o') : 46,
    ('..ooo......o....o.ooooo.o..oo...o@@ooo.@.@@@.oo@...@@@.@...ooo..', 'o') : 25,
    ('..ooo.....oo....ooooooo.oo@oo.@.ooo@o@@@oooo@o@@..o@o@.@..oooo..', 'o') : 31,
    ('...........................o@......o@@.....o@o.....@............', 'o') : 59,
    ('...........................ooo@....oo@.o...o@oo....@.o....@@@@@.', 'o') : 21,
    ('.....................o.@...oooo@...oooo@..@@@@@@...@.o....@@@@@.', 'o') : 52,
    ('.............@.......@@@...oo@@@@.oo@o@@oooooo@@..@@oo....@@@@@.', 'o') : 24,
    ('...ooo....@.@@.....@@@@@o..o@o@@o.oo@o@@oooooo@@..@@oo....@@@@@.', 'o') : 17}
winnables = [
    [ 0,  1,  2,  3,  4,  5,  6,  7],
    [ 0,  8, 16, 24, 32, 40, 48, 56],
    [ 0,  9, 18, 27, 36, 45, 54, 63], 
    [ 1,  9, 17, 25, 33, 41, 49, 57], 
    [ 1, 10, 19, 28, 37, 46, 55], 
    [ 2, 10, 18, 26, 34, 42, 50, 58], 
    [ 2, 11, 20, 29, 38, 47], 
    [ 2,  9, 16], 
    [ 3, 11, 19, 27, 35, 43, 51, 59], 
    [ 3, 12, 21, 30, 39], 
    [ 3, 10, 17, 24], 
    [ 4, 12, 20, 28, 36, 44, 52, 60], 
    [ 4, 13, 22, 31], 
    [ 4, 11, 18, 25, 32], 
    [ 5, 13, 21, 29, 37, 45, 53, 61], 
    [ 5, 14, 23], 
    [ 5, 12, 19, 26, 33, 40], 
    [ 6, 14, 22, 30, 38, 46, 54, 62], 
    [ 6, 13, 20, 27, 34, 41, 48], 
    [ 7, 15, 23, 31, 39, 47, 55, 63], 
    [ 7, 14, 21, 28, 35, 42, 49, 56], 
    [ 8,  9, 10, 11, 12, 13, 14, 15], 
    [16, 17, 18, 19, 20, 21, 22, 23], 
    [ 8, 17, 26, 35, 44, 53, 62], 
    [15, 22, 29, 36, 43, 50, 57], 
    [24, 25, 26, 27, 28, 29, 30, 31], 
    [16, 25, 34, 43, 52, 61], 
    [23, 30, 37, 44, 51, 58], 
    [32, 33, 34, 35, 36, 37, 38, 39], 
    [24, 33, 42, 51, 60], 
    [31, 38, 45, 52, 59], 
    [40, 41, 42, 43, 44, 45, 46, 47], 
    [32, 41, 50, 59], 
    [39, 46, 53, 60], 
    [48, 49, 50, 51, 52, 53, 54, 55], 
    [40, 49, 58], 
    [47, 54, 61], 
    [56, 57, 58, 59, 60, 61, 62, 63]]
newIndexing = {
     0:11, 1:12, 2:13, 3:14, 4:15, 5:16, 6:17, 7:18,
     8:21, 9:22,10:23,11:24,12:25,13:26,14:27,15:28,
    16:31,17:32,18:33,19:34,20:35,21:36,22:37,23:38,
    24:41,25:42,26:43,27:44,28:45,29:46,30:47,31:48,
    32:51,33:52,34:53,35:54,36:55,37:56,38:57,39:58,
    40:61,41:62,42:63,43:64,44:65,45:66,46:67,47:68,
    48:71,49:72,50:73,51:74,52:75,53:76,54:77,55:78,
    56:81,57:82,58:83,59:84,60:85,61:86,62:87,63:88, -1:-1}
weights = [
     10, -80, 5, 5, 5, 5, -40, 10,
    -80,-120, 0,-1,-1, 0,-120,-40,
      5,   0, 1,.5,.5, 1,   0,  5,
      5,  -1,.5, 0, 0,.5,  -1,  5,
      5,  -1,.5, 0, 0,.5,  -1,  5,
      5,   0, 1,.5,.5, 1,   0,  5,
    -80,-120, 0,-1,-1, 0,-120,-80,
     10, -80, 5, 5, 5, 5, -80, 10]
weightsB = [
      0, -80,30,30,30,30, -50,  0,
    -50,-100, 1, 1, 1, 1,-100,-50,
     30,   1, 2, 2, 2, 2,   1, 30,
     30,   1, 2, 1, 1, 2,   1, 30,
     30,   1, 2, 1, 1, 2,   1, 30,
     30,   1, 2, 2, 2, 2,   1, 30,
    -50,-100, 1, 1, 1, 1,-100,-50,
      0, -50,30,30,30,30, -50,  0]
def printFormat(pzl, a):
    for n in range(a): print(pzl[n*a:(n+1)*a])
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
            if sym == '@':
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
        if sym == '@':
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
def midHeuristic(board, token):
    n, poss, poss2 = 0, genPossible(board, switch[token]), genPossible(board, token)
    for c in corners:
        if board[c] == token: n += 10000
        elif board[c] == token: n -= 10000
        elif c in poss: n -= 100
        elif c in poss2: n += 100
    if board[0] == token: weights[9] = 20
    if board[7] == token: weights[14] = 20
    if board[56] == token: weights[49] = 20
    if board[63] == token: weights[54] = 20
    for num in range(64):
        if board[num] == token:
            if securePiece(board, num, token): n += 500
            else: n += weightsB[num]
        elif board[num] == switch[token]:
            if securePiece(board, num, switch[token]): n -= 500
            else: n -= weightsB[num]
    n -= len(poss) * 100
    print(board, token, n)
    return n
def heuristicMove(board, token, indx):
    n = 0
    g, f, p, p2 = board.count(token)-board.count(switch[token]), board.count('.'), genPossible(board, switch[token]), genPossible(board, token)
    y = len(p)
    if not p and not p2: n += (g^3)*10
    for c in corners: 
        if board[c] == token: n += 100
        elif board[c] == switch[token]: n -= 100
    if f > 45: n += 500-(100*y)
    elif f > 30 or f < 15: n += 100/(2**y)
    elif y > 4: n += 5-y
    else: n += 1000*(math.factorial(5-y)/math.factorial(y))
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
            if securePiece(board, num, token): n += 30
            else: n += weights[num]
        elif board[num] == switch[token]:
            if securePiece(board, num, switch[token]): n -= 30
            else: n -= weights[num]
    for m in p:
        if m in corners: n -= 1000
    for m in p2:
        if m in corners: n += 5
    n *= (random.random()*.2+.9)
    return n
def midGame(brd, token, indx, level, player):
    poss = genPossible(brd, token)
    poss2 = genPossible(brd, switch[token])
    score = midHeuristic(brd, player)
    if level == 0: return score, indx
    if not poss:
        if not poss2: return score, indx
        token = switch[token]
        indx = [-1] + indx
        poss, poss2 = poss2, poss
    nmList = [midGame(placeChar(new_indx, brd, token), switch[token], [new_indx] + indx, level-1, player) for new_indx in poss]
    if token == player: return max(nmList)
    else: return min(nmList)
class Strategy():
    def best_strategy(self, board, player, best_move, running):
        if running.value:
            pzl = board.replace('?','')
            period = pzl.count('.')
            dummy = -1
            pzl90, pzl180, pzl270 = flipVertical(transpose(pzl)), pzl[::-1], flipHorizontal(transpose(pzl))
            if (pzl, player) in moveSel: best_move.value = newIndexing[moveSel[(pzl, player)]]
            elif (pzl90, player) in moveSel: best_move.value = newIndexing[calculatePosition(moveSel[(pzl90, player)], 90)]
            elif (pzl180, player) in moveSel: best_move.value = newIndexing[calculatePosition(moveSel[(pzl180, player)], 180)]
            elif (pzl270, player) in moveSel: best_move.value = newIndexing[calculatePosition(moveSel[(pzl270, player)], 270)]
            elif period > 11:
                n = 3
                while running.value:
                    best_move.value = newIndexing[midGame(pzl, player, [], n, player)[1][-1]]
                    n += 1
            else: best_move.value = newIndexing[alphaBeta(pzl, player, -64, 64)[-1]]