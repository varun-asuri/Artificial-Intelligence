import math
import sys
import time
import re

startTime = time.time()
sys.setrecursionlimit(1000000000)
cache = {}
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
statement = re.compile('[^#]{3}')
dimensions = [int(d) for d in sys.argv[1].split('x')]
dimensions += [dimensions[0] * dimensions[1]]
dimensions += [dimensions[2]//2]
limits = [[-1, -1, -1, -1] for num2 in range(dimensions[2])]
increment = {'H' : 1, 'V' : dimensions[1]}
for x in range(dimensions[2]):
    div, mod = divmod(x, dimensions[1])
    limits[x][0] = div*dimensions[1]+max(0, mod-2)
    limits[x][1] = div*dimensions[1]+min(dimensions[1], mod+3)
    limits[x][2] = mod+max(0, (div-2)*dimensions[1])
    limits[x][3] = mod+min((div+2)*dimensions[1]+1, dimensions[2]-1)
board = '-' * dimensions[2]
buffers = int(sys.argv[2])
file = open(sys.argv[3], 'r')
words = sys.argv[4:]
for raw in words:
    regex = re.match('^(.)(\d+)x(\d+)(.+)$', raw)
    orient, spot, obj = increment[regex.group(1).upper()], int(regex.group(2)) * dimensions[1] + int(regex.group(3)), regex.group(4).upper()
    for s, o in enumerate(obj):
        indx = spot+(s*orient)
        board = board[:indx] + o + board[indx+1:]
        if o == '#':
            reverse = dimensions[2]-indx-1
            if reverse != indx: board = board[:reverse] + o + board[reverse+1:]
buffers -= board.count('#')
if buffers%2:
    board = board[:dimensions[3]] + '#' + board[dimensions[3]+1:]
    buffers -= 1
def fill(area, row, col):
    if (area, row, col) in cache: return cache[(area, row, col)]
    indx = row*dimensions[1]+col
    if area[indx] != '#':
        area = area[:indx] + '#' + area[indx+1:]
        if row: area = fill(area, row-1, col)
        if col: area = fill(area, row, col-1)
        if row < dimensions[0]-1: area = fill(area, row+1, col)
        if col < dimensions[1]-1: area = fill(area, row, col+1)
    cache[(area, row, col)] = area
    return area
def filledBlocks(board):
    div, mod = divmod(board.find('-'), dimensions[1])
    board = fill(board, div, mod)
    hashtags = board.count('#')
    if hashtags == dimensions[2]: return board
    return ""
def antiClumping(board, indx):
    up, down, left, right = indx, indx, indx, indx
    div, mod = divmod(indx, dimensions[1])
    up, down, left, right = board[mod:indx+1:dimensions[1]][::-1], board[indx:dimensions[2]:dimensions[1]], board[div*dimensions[1]:indx+1][::-1], board[indx:(div+1)*dimensions[1]]
    if '#' in up: up = up[:up.find('#')]
    if '#' in down: down = down[:down.find('#')]
    if '#' in left: left = left[:left.find('#')]
    if '#' in right: right = right[:right.find('#')]
    up, down, left, right = len(up), len(down), len(left), len(right)
    if {up, down, left, right} & {2, 3}: return 0
    return (up*down+left*right)/5 + up+down+left+right
def isInvalid(board):
    for a in range(dimensions[2]):
        if board[a] == '#': continue
        if not statement.search(board[limits[a][0]:limits[a][1]]) or not statement.search(board[limits[a][2]:limits[a][3]:dimensions[1]]): return "", a
    return board, -1
def bruteForce(board, buffers):
    valid = isInvalid(board)
    while not valid[0]:
        if buffers and valid[1] != dimensions[3]:
            board = board[:valid[1]] + '#' + board[valid[1]+1:dimensions[2]-valid[1]-1] + '#' + board[dimensions[2]-valid[1]:]
            buffers -= 2
            valid = isInvalid(board)
        else: return ''
    if not filledBlocks(board): return ""
    if not buffers: return board
    heuristical = sorted([(antiClumping(board, n), n) for n in range(dimensions[3]) if board[n] == '-'], reverse=True)
    for antiClump in heuristical:
        newBoard = board[:antiClump[1]] + '#' + board[antiClump[1]+1:dimensions[2]-antiClump[1]-1] + '#' + board[dimensions[2]-antiClump[1]:]
        bF = bruteForce(newBoard, buffers-2)
        if bF: return bF
    return ''
print()
if dimensions[2] == buffers or dimensions[2]%2 and dimensions[2]-1 == buffers: board = '#' * dimensions[2]
else: board = bruteForce(board, buffers)
for a in range(dimensions[0]): print(board[a*dimensions[1]:(a+1)*dimensions[1]])