import time
import math
import sys
import random
import tkinter
import heapq
from distanceDemo import calcd

startTime = time.time()
c1, c2, c3, c4, c5 = 'deeppink', '#125699', 'springgreen', '#0D0222', 'white'

# TKINTER SETUP
tk = tkinter.Tk()
tk.title('Railroad with A*')
tk.geometry('720x480')
canvas = tkinter.Canvas(tk, width = 720, height = 480, background = c4)
canvas.pack(fill = 'both', expand = 1)

# FILE DATA EXTRACTION
nodeFile = open('rrNodes.txt', 'r').read().splitlines()
edgeFile = open('rrEdges.txt', 'r').read().splitlines()
cityFile = open('rrNodeCity.txt', 'r').read().splitlines()
nodes = {}
edges = {}
cities = {}
values = {}
for n in nodeFile:
    line = n.split(' ')
    nodes[line[0]] = (line[1], line[2])
for e in edgeFile:
    line = e.split(' ')
    if line[0] not in edges:
        edges[line[0]] = []
    if line[1] not in edges:
        edges[line[1]] = []
    edges[line[0]].append(line[1])
    edges[line[1]].append(line[0])
for c in cityFile:
    line = c.split(' ')
    cities[' '.join(line[1:])] = line[0]
    values[line[0]] = ' '.join(line[1:])

# CREATION OF BASE MAP
def drawLine(x1, y1, x2, y2, color):
    x1, x2, y1, y2 = float(x1), float(x2), float(y1), float(y2)
    canvas.create_line(720-(y1*-10-590), 480-(x1*10-135), 720-(y2*-10-590), 480-(x2*10-135), fill=color)
for line in edgeFile:
    a = line.split(' ')
    n1, n2 = a[0], a[1]
    drawLine(*nodes[n1], *nodes[n2], c5)
tk.update()

def error():
    print()
    print('ERROR: City not found')
    tk.destroy()

# ACCESSING SYS ARGUMENTS
start = sys.argv[1]
finish = sys.argv[2]
if len(sys.argv) > 3:
    if sys.argv[1] in cities:
        start = sys.argv[1]
        finish = ' '.join(sys.argv[2:])
    else:
        start = ' '.join(sys.argv[1:3])
        finish = ' '.join(sys.argv[3:])
else:
    start = sys.argv[1]
    finish = sys.argv[2]
if start in cities:
    start = cities[start]
if finish in cities:
    finish = cities[finish]

# A* ALGORITHM
def solve(loc, d):
    c_draw = set()
    o_lines = {}
    init_h = calcd(*nodes[loc], *nodes[d])
    closedSet = set()
    startTime = time.time()
    openSet = []
    openSet.append( (init_h, 0, loc) )
    dictionary = {loc: ("", init_h)}
    while openSet:
        old_h, level, loc = openSet.pop(0)
        if loc in closedSet:
            continue
        closedSet.add(loc)
        if dictionary[loc][0] != "":
            drawLine(*nodes[loc], *nodes[dictionary[loc][0]], c2)
        if loc in o_lines:
            for x in edges[loc]:
                drawLine(*nodes[loc], *nodes[x], c2)
            del o_lines[loc]
        c_draw.add(loc)
        if loc == d:
            a = []
            x = loc
            while x != "":
                if x in values:
                    a.append(values[x])
                else:
                    a.append(x)
                if dictionary[x][0] != "":
                    drawLine(*nodes[x], *nodes[dictionary[x][0]], c3)
                    tk.update()
                x = dictionary[x][0]
            tk.update()
            print()
            for pos in a:
                if pos in cities:
                    pos = cities[pos]
                raw = dictionary[pos][0]
                if raw in values:
                    raw = values[raw]
                if dictionary[pos][0] != "":
                    print(raw, '-', calcd(*nodes[pos], *nodes[dictionary[pos][0]]))
            tk.update()
            print()
            print("Distance:", old_h)
            print("Length:", level)
            print("ClosedSet:", len(closedSet))
            print("OpenSet:", len(openSet)+len(closedSet))
            print("Time: ", time.time()-startTime, "s", sep='')
            return
        a = edges[loc]
        for x in a:
            if x not in closedSet and x not in openSet:
                f = calcd(*nodes[x], *nodes[d]) + old_h - calcd(*nodes[loc], *nodes[d]) + calcd(*nodes[loc], *nodes[x])
                if x not in dictionary or f <= dictionary[x][1]:
                    dictionary[x] = (loc, f)
                openSet.append( (f, level+1, x) )
                drawLine(*nodes[x], *nodes[loc], c1)
                o_lines[x] = loc
        if len(c_draw)**1.25 > len(closedSet):
            tk.update()
            c_draw = set()
        openSet.sort()

if start not in nodes or finish not in nodes:
    error()
else:
    solve(start, finish)
tk.mainloop()