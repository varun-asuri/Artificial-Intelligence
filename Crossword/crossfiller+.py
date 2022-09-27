import math, sys, time, re, random

startTime = [time.time(), time.time()]
outputFile = open('output.txt', 'w')
sys.setrecursionlimit(1000000000)
cache, values, alphadict = {}, {'A':11178,'B':2516,'C':6030,'D':5139,'E':15332,'F':1911,'G':3606,'H':3018,'I':11131,'J':368,'K':1295,'L':6761,'M':3953,'N':9810,'O':8751,'P':4051,'Q':256,'R':10008,'S':10427,'T':9378,'U':3998,'V':1688,'W':1350,'X':534,'Y':2130,'Z':349}, {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}
statement = re.compile('[^#]{3}')
dimensions = [int(d) for d in sys.argv[1].split('x')]
dimensions += [dimensions[0] * dimensions[1]]
dimensions += [dimensions[2]//2, max(dimensions[0], dimensions[1])]
limits = [[-1, -1, -1, -1] for num2 in range(dimensions[2])]
increment = {'H' : 1, 'V' : dimensions[1]}
for x in range(dimensions[2]):
    div, mod = divmod(x, dimensions[1])
    limits[x][0] = div*dimensions[1]+max(0, mod-2)
    limits[x][1] = div*dimensions[1]+min(dimensions[1], mod+3)
    limits[x][2] = mod+max(0, (div-2)*dimensions[1])
    limits[x][3] = mod+min((div+2)*dimensions[1]+1, dimensions[2]-1)
board, high, buffers, best, dictionary, preprocess, file = '-' * dimensions[2], dimensions[2], int(sys.argv[2]), dimensions[2]-buffers, [set() for a in range(dimensions[4]-2)], [set() for b in range(dimensions[4]*26)], open(sys.argv[3], 'r')
for raw in file:
    nL = raw.rstrip().upper()
    l = len(nL)
    if l > dimensions[4] or l < 3 or '/' in nL: continue
    dictionary[l-3].add(nL)
    for d, o in enumerate(nL):
        if o.isLetter(): preprocess[d*26+alphadict[o]].add(nL)
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
best2 = buffers
if buffers%2:
    board = board[:dimensions[3]] + '#' + board[dimensions[3]+1:]
    buffers -= 1 
def calcLimits(board):
    arr = []
    for indx in range(dimensions[2]):
        if board[indx] == '#':
            arr.append([-1, -1, -1, -1, -1, -1])
            continue
        div, mod = divmod(indx, dimensions[1])
        svb, sva, shb, sha = board[mod:indx+1:dimensions[1]][::-1], board[indx:dimensions[2]:dimensions[1]], board[div*dimensions[1]:indx+1][::-1], board[indx:(div+1)*dimensions[1]]
        if '#' in svb: svb = svb[:svb.find('#')]
        if '#' in sva: sva = sva[:sva.find('#')]
        if '#' in shb: shb = shb[:shb.find('#')]
        if '#' in sha: sha = sha[:sha.find('#')]
        arr.append([indx-(len(svb)-1)*dimensions[1], indx+(len(sva)-1)*dimensions[1]+1, indx-len(shb)+1, indx+len(sha), len(svb)-1, len(shb)-1, indx])
    return arr
def repeating(board, lims):
    words = {}
    visited = set()
    for r in range(dimensions[2]):
        if board[r] == '#': continue
        if r in visited: continue
        sv, sh = board[lims[r][0]:lims[r][1]:dimensions[1]], board[lims[r][2]:lims[r][3]]
        visV, visH = set(range(lims[r][0],lims[r][1],dimensions[1])), set(range(lims[r][2],lims[r][3]))
        visited = visited.union(visV).union(visH)
        if '-' not in sv:
            if sv in words and words[sv] != (lims[r][0], lims[r][1]): return ''
            words[sv] = (lims[r][0], lims[r][1])
        if '-' not in sh:
            if sh in words and words[sh] != (lims[r][2], lims[r][3]): return ''
            words[sh] = (lims[r][2], lims[r][3])
    return board
def fill(area, row, col):
    if (area, row, col) in cache: return cache[(area, row, col)]
    indx = row*dimensions[1]+col
    if area[indx] != '#':
        area = area[:indx] + '#' + area[indx+1:]
        if row: area = fill(area, row-1, col)
        if area == '#' * dimensions[2]: return area
        if col: area = fill(area, row, col-1)
        if area == '#' * dimensions[2]: return area
        if row < dimensions[0]-1: area = fill(area, row+1, col)
        if area == '#' * dimensions[2]: return area
        if col < dimensions[1]-1: area = fill(area, row, col+1)
        if area == '#' * dimensions[2]: return area
    cache[(area, row, col)] = area
    return area
def fillHelper(board):
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
def bruteForce2(board, lims, high):
    print(board, file=outputFile)
    if not repeating(board, lims): return ''
    if not high: return board
    judic =  [(math.inf, []) for i in range(dimensions[2])]
    for indx in range(dimensions[2]):
        if board[indx] != '-': continue
        div, mod = divmod(indx, dimensions[1])
        sv, sh = board[lims[indx][0]:lims[indx][1]:dimensions[1]], board[lims[indx][2]:lims[indx][3]]
        if (sv, sh, lims[indx][4], lims[indx][5]) in cache:
            possChars = cache[(sv, sh, lims[indx][4], lims[indx][5])]
            if not possChars: return ''
            if len(possChars) == 1:
                newBoard = board[:indx] + possChars[0][1] + board[indx+1:]
                return bruteForce2(newBoard, lims, high-1)
            judic[indx] = (indx, possChars)
            continue
        wordsV, wordsH, possV, possH = dictionary[len(sv)-3], dictionary[len(sh)-3], {}, {}
        for u, v in enumerate(sv):
            if v != '-': wordsV = wordsV & preprocess[u*26+alphadict[v]]
        if not wordsV: return ''
        for u, h in enumerate(sh):
            if h != '-': wordsH = wordsH & preprocess[u*26+alphadict[h]]
        if not wordsH: return ''
        for vword in wordsV:
            char = vword[lims[indx][4]]
            if char in possV: possV[char] += 1
            else: possV[char] = 1
        for hword in wordsH:
            char = hword[lims[indx][5]]
            if char in possH: possH[char] += 1
            else: possH[char] = 1
        possChars = []
        for c in possV.keys()&possH.keys(): possChars.append( (-possV[c]-possH[c]-(values[c]/10000), c) )
        if not possChars:
            cache[(sv, sh, lims[indx][4], lims[indx][5])] = ''
            return ''
        if len(possChars) == 1:
            cache[(sv, sh, lims[indx][4], lims[indx][5])] = possChars
            newBoard = board[:indx] + possChars[0][1] + board[indx+1:]
            return bruteForce2(newBoard, lims, high-1)
        possChars.sort()
        if sv.count('-') - 1 and sh.count('-') - 1: cache[(sv, sh, lims[indx][4], lims[indx][5])] = possChars
        judic[indx] = (indx, possChars)
    judic = min(judic, key=lambda item: len(item[1])*100+item[0])
    for p in judic[1]:
        newBoard = board[:judic[0]] + p[1] + board[judic[0]+1:]
        bF = bruteForce2(newBoard, lims, high-1)
        if bF: return bF
    return ''
def bruteForce(board, buffers):
    valid = isInvalid(board)
    while not valid[0]:
        if buffers and valid[1] != dimensions[3]:
            board = board[:valid[1]] + '#' + board[valid[1]+1:dimensions[2]-valid[1]-1] + '#' + board[dimensions[2]-valid[1]:]
            buffers -= 2
            valid = isInvalid(board)
        else: return ''
    if not fillHelper(board): return ""
    if not buffers:
        print(board, file=outputFile)
        return bruteForce2(board, calcLimits(board), board.count('-'))
    heuristical = sorted([(antiClumping(board, n), n) for n in range(dimensions[3]) if board[n] == '-'], reverse=True)
    for antiClump in heuristical:
        newBoard = board[:antiClump[1]] + '#' + board[antiClump[1]+1:dimensions[2]-antiClump[1]-1] + '#' + board[dimensions[2]-antiClump[1]:]
        bF = bruteForce(newBoard, buffers-2)
        if bF: return bF
    return ''
if dimensions[2] == buffers or dimensions[2]%2 and dimensions[2]-1 == buffers: board = '#'*dimensions[2]
else: board = bruteForce(board, buffers)
print(board, file=outputFile)