import time
import math
import sys
import random

beginTime = time.time()
file = open(sys.argv[1], 'r').read().splitlines()
goal = file[0]
size = int(math.sqrt(len(goal)))
default = {goal[0]:0, goal[1]:1, goal[2]:2, goal[3]:3, goal[4]:4, goal[5]:5, goal[6]:6, goal[7]:7, goal[8]:8, goal[9]:9, goal[10]:10, goal[11]:11, goal[12]:12, goal[13]:13, goal[14]:14, goal[15]:15}

lookUp = [[-1 for x in range(size**2)] for x in range(size**2)]
lookUp3 = {}

def solve(puzzle, goals):
    done = set()
    # initial = puzzle
    startTime = time.time()
    # tms = 0
    # for b in range(size):
    #     print(initial[size*b:size*(b+1)])
    md = 0
    for ch in puzzle:
        n = puzzle.index(ch)
        if ch != '_':
            if ch in default:
                ch = default[ch]
            parsed = int(ch)
            d = lookUp[parsed][n]
            if d == -1:
                myY, myX = divmod(parsed, size)
                realY, realX = divmod(n, size)
                d = abs(myY-realY)+abs(myX-realX)
                lookUp[parsed][n] = d
            md += d
    # print(md)
    parseMe = [[] for x in range(80)]
    parseMe[md+0].append(puzzle)
    # parseMe = [ (md+0, puzzle) ]
    nonempties = {md}
    # dictionary = {puzzle:""}
    levels = {puzzle:0}
    svbl = True
    count1 = 0
    count2 = 0
    usable1 = list(puzzle[:].replace('_',''))
    usable2 = list(goal[:].replace('_',''))
    for n in range((size**2)-1):
        if usable1[n] in default:
            usable1[n] = str(default[usable1[n]]+1)
        if usable2[n] in default:
            usable2[n] = str(default[usable2[n]]+1)
    for a in range(len(usable1)): 
        for b in range(a + 1, len(usable1)):
            if int(usable1[a]) > int(usable1[b]): 
                count1 += 1
    for a in range(len(usable2)): 
        for b in range(a + 1, len(usable2)): 
            if int(usable2[a]) > int(usable2[b]): 
                count2 += 1
    row1 = 4-puzzle.find('_')//size
    diff1 = abs(count1-count2)
    diff2 = abs(4-row1)
    if bool(size%2) and bool(diff1%2):
        svbl = False
    elif not bool(size%2) and ((diff2%2)==(diff1%2)):
        svbl = False
    if svbl:
        while parseMe:
            if time.time() - startTime > 40:
                # totalTime = time.time()-startTime
                # print("Time: ", totalTime, "s", sep='')
                # print(tms)
                return -1
            minimum = min(nonempties)
            # startTime = time.time()
            puzzle = parseMe[minimum].pop(-1)
            # tms += time.time()-startTime
            if(len(parseMe[minimum]) == 0):
                nonempties.remove(minimum)
            if puzzle in done:
                continue
            done.add(puzzle)
            if puzzle == goal:
                # a = []
                # x = puzzle
                # while x != "":
                #     a.append(x)
                #     x = dictionary[x]
                # print()
                # print("Steps:", len(a)-1)
                # totalTime = time.time()-startTime
                # print("Time: ", totalTime, "s", sep='')
                # print()
                # print(tms)
                # return len(a)-1
                return minimum
            a = []
            b = puzzle.index("_")
            if b > size-1:
                a.append( puzzle[0: b-size] + puzzle[b] + puzzle[b-size+1:b] + puzzle[b-size] + puzzle[b+1:] )
            if b > 0 and b % size:
                a.append( puzzle[0: b-1] + puzzle[b] + puzzle[b-1] + puzzle[b+1:] )
            if b < len(puzzle)-1 and b % size != size-1:
                a.append( puzzle[0: b] + puzzle[b+1] + puzzle[b] + puzzle[b+2:] )
            if b < len(puzzle)-size:
                a.append( puzzle[0: b] + puzzle[b+size] + puzzle[b+1:b+size] + puzzle[b] + puzzle[b+size+1:] )
            for x in a:
                if x not in done:
                    num = 0
                    if x in lookUp3:
                        num = lookUp3[x]
                    else:
                        num = 0
                        for n, ch in enumerate(x):
                            if ch != '_':
                                if ch in default:
                                    ch = default[ch]
                                parsed = int(ch)
                                d = lookUp[parsed][n]
                                if d == -1:
                                    myY, myX = divmod(parsed, size)
                                    realY, realX = divmod(n, size)
                                    d = abs(myY-realY)+abs(myX-realX)
                                    lookUp[parsed][n] = d
                                num += d
                        lookUp3[x] = num
                    lev = levels[puzzle]+1
                    # dictionary[x] = puzzle
                    levels[x] = lev
                    parseMe[lev+num].append(x)
                    nonempties.add(lev+num)
                    # parseMe.append( ((lev+num), x) )
            # parseMe.sort()
    # print()
    # print("Steps: -1")
    # totalTime = time.time()-startTime
    # print("Time: ", totalTime, "s", sep='')
    # print()
    # print(tms)
    return -1
    
# beginTime = time.time()
# if len(sys.argv) == 2:
#    print(solve(sys.argv[1], 'ABCDEFGHIJKLMNO_', beginTime))
# else:
#    print(solve(sys.argv[1], sys.argv[2], beginTime))

count = [0]*len(file)
solvables = []
unsolvables = 0
print()
y = 0
n = 0
for n in range(len(file)):
    # if time.time()-beginTime > 120:
    #     break
    puzzle = file[n]
    startTime = time.time()
    x = solve(puzzle, goal)
    totalTime = time.time()-startTime
    # if x != n:
    #     x -= 2
    if x == -2:
        y = totalTime
        break
    if x == n:
        count[n] = 1
    if x == -1:
        unsolvables += 1
    else:
        solvables.append(x)
    print("Pzl ", n, ": ", puzzle, " => ", x, " steps\t\tin ", str(totalTime)[:4], "s", sep='')
finalTime = time.time()
print()
print("Impossible Count:", unsolvables)
print("Avg len for possibles:", sum(solvables)/len(solvables))
print("Solved ", n, " puzzles in ", str(finalTime-beginTime)[:4] , "s", sep='')
print()
# if totalTime > 15:
#     print("Excess Time: ", str(totalTime)[:4], "s", sep='')
x = 1
if n-len(count) > 0:
    x = .9
print("Final Grade: ", n*100/53*x, "%", sep='')
print()
print('The evaluation is: ', end='')
print(sum(count[:30]), '+', sum(count[30:40]), '+', sum(count[40:]))

# iterations = 10
# numtrials = 500
# times = []
# if len(sys.argv) > 1:
#     iterations = int(sys.argv[1])
# if len(sys.argv) > 2:
#     numtrials = int(sys.argv[2])
# for t in range(iterations):
#     beginTime = time.time()
#     unsolvables = 0
#     totsteps = 0
#     for n in range(numtrials):
#         arr = list("12345678_")
#         random.shuffle(arr)
#         puzzle = ''.join(arr)
#         steps, svbl = solve(puzzle, 'ABCDEFGHIJKLMNO_')
#         unsolvables += svbl
#         if steps != -1:
#             totsteps += steps
#     finalTime = time.time()-beginTime
#     times.append(finalTime)
#     print("Trial Number:", t+1)
#     print("Final Time: ", finalTime, "s", sep='')
#     print("Unsolvables:", unsolvables)
#     print("Average Steps:", totsteps/(numtrials-unsolvables))
#     print()
# print("Shortest Time: ", min(times), "s", sep='')