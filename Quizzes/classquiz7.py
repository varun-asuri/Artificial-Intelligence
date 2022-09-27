import sys
import math

pzl = sys.argv[1]
height = 0
width = 0
if len(sys.argv) <= 2:
    height = math.floor(len(pzl)**.5)
    while len(pzl) % height: height -= 1
    width = len(pzl) // height
else:
    width = int(sys.argv[2])
    height = len(pzl) // width

def flipVertical(pzl):
    newPzl = ''
    for n in range(height):
        row = pzl[n*width: (n+1)*width]
        newPzl += row[::-1]
    return newPzl

def flipHorizontal(pzl):
    newPzl = ''
    for n in range(height):
        row = pzl[n*width: (n+1)*width]
        newPzl = row + newPzl
    return newPzl

def transpose(pzl):
    newPzl = ''
    for n in range(width):
        col = pzl[n:len(pzl):width]
        newPzl += col
    return newPzl

t = transpose(pzl)
part1 = [('normal', pzl), ('reverse', pzl[::-1]), ('vertflip', flipVertical(pzl)), ('horizflip', flipHorizontal(pzl)), ('trans', t), ('transrev', t[::-1])]
width, height = height, width
part2 = [('90clock - vertflip(trans)', flipVertical(t)), ('90cclock - horizflip(trans)', flipHorizontal(t))]
total = part1 + part2
for s, p in total:
    print(s)
    for h in range(height): print(p[h*width:(h+1)*width])
    print()