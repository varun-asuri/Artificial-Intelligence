import time
import math
import sys

startTime = time.time()
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SOLUTION = []
s = ' '.join(sys.argv[1:]).replace('x', ' ').replace('X', ' ').replace('"', '').split(' ')
BLOCKS = [(int(s[i])*int(s[i+1]), int(s[i]), int(s[i+1])) for i in range(2,len(s),2)]
CONTAINER = (int(s[0])*int(s[1]), int(s[1]), int(s[0]))
BLOCKS.sort()
REMAIN, USED = BLOCKS.copy(), []
CURRENT = [['.' * CONTAINER[1]] * CONTAINER[2]]

def bailOut1():
    subArea = 0
    for b in BLOCKS: subArea += b[0]
    return CONTAINER[0] < subArea

def bailOut2():
    if not CONTAINER[1] % 2 and not CONTAINER[2] % 2: return False
    for b in BLOCKS:
        if b[1] % 2 or b[2] % 2: return False
    return True

def bailOut3():
    b = ''
    if len(BLOCKS) == 1 and BLOCKS[0][1] in CONTAINER:
        b = str(CONTAINER[2]) + 'x' + str(CONTAINER[1])
        SOLUTION.append(b)

def findSpot():
    for i, n in enumerate(CURRENT[-1]):
        for i2, n2 in enumerate(n):
            if n2 == '.': return (i2, i)

def editGrid(indx, b):
    g = CURRENT[-1].copy()
    for i in range(indx[1], indx[1]+b[2]):
        g[i] = g[i][:indx[0]] + (ALPHA[len(USED)] * b[1]) + g[i][indx[0]+b[1]:]
    return g

def areaRemaining(indx):
    lim = CONTAINER[1]
    for i, w in enumerate(CURRENT[-1][indx[1]][indx[0]:]):
        if w != '.':
            lim = i
            break
    width = lim - indx[0]
    height = 0
    for n in range(indx[1], CONTAINER[2]):
        if CURRENT[-1][n][indx[0]:lim] == ('.' * width): height += 1
        else: break
    return (width, height) 

def setOfChoices():
    indx = findSpot()
    space = areaRemaining(indx)
    for b in REMAIN[::-1]:
        if b[1] <= space[0] and b[2] <= space[1]:
            g = editGrid(indx, b)
            yield g, b, 0
        b2 = (b[0], b[2], b[1])
        if b2[1] <= space[0] and b2[2] <= space[1]:
            g2 = editGrid(indx, b2)
            yield g2, b2, 1

def bruteForce():
    if len(REMAIN) == 0: return 1

    for new_g, sub, rev in setOfChoices():
        
        CURRENT.append(new_g)
        if rev:
            REMAIN.remove( (sub[0], sub[2], sub[1] ) )
        else:
            REMAIN.remove(sub)
        USED.append(sub)

        bF = bruteForce()
        if bF: return 1

        CURRENT.pop()
        if rev:
            REMAIN.append( (sub[0], sub[2], sub[1] ) )
        else:
            REMAIN.append(sub)
        REMAIN.sort()
        USED.pop()
    
    return 0

def fullScan(extend, indx, space):
    letters = set()
    indx = indx[1]*CONTAINER[1] + indx[0]
    for n in extend[indx:]:
        if n != '.': letters.add(n)
    toDel = set()
    for n in letters:
        if extend.find(n) < indx: toDel.add(n)
    letters = letters - toDel
    if letters:
        return ALPHA.find(min(letters))
    else:
        return len(USED)

def finalSlot(indx):
    width = 0
    height = 0
    for x in CURRENT[-1][indx[1]][indx[0]:]:
        if x == '.': width += 1
        else: break
    for x in CURRENT[-1][indx[1]:]:
        if x[indx[0]] == '.': height += 1
        else: break
    return width, height

def fillIn(extend):
    indx = findSpot()
    space = finalSlot(indx)
    space = (space[0]*space[1], space[0], space[1])
    g = editGrid(indx, space)
    CURRENT.append(g)
    USED.insert(fullScan(extend, indx, space), space)

def readDimensions():
    for b in USED:
        width = b[1]
        height = b[2]
        s = str(height)+'x'+str(width)
        SOLUTION.append(s)

if bailOut1() or bailOut2():
    print('\nNo Solution')
else:
    bailOut3()
    if not SOLUTION:
        bruteForce()
        extend = ''.join(CURRENT[-1])
        while extend.find('.') != -1 and extend.count('.') != CONTAINER[0]:
            fillIn(extend)
            extend = ''.join(CURRENT[-1])
        readDimensions()
    print('\nDecomposition:', end=' ')
    print(*SOLUTION)
    print(*CURRENT[-1], sep='\n')

print('Time: ', time.time()-startTime, 's', sep='')