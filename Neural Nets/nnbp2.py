import math, time, sys, random, re

startTime, alpha, invals, i_use, answers, errsum, minerrsum, layercts = time.time(), 0.1, [], [], [], 0.01, 0.02, [3, 8, 2, 1, 1]
raw, cutoff, sign, radius,  = sys.argv[1][7:], 1, '', 0
if raw[1] == '=': cutoff = 2
sign, radius = raw[:cutoff], float(raw[cutoff:])**.5
for num in range(3000):
    x, y, c = random.random()*3.0-1.5, random.random()*3.0-1.5, random.random()
    if c < .55:
        x, y = random.random()*radius*2-radius, random.random()*radius*2-radius
        if c < .1375: x = (radius**2-y**2)**.5
        elif c < .275: x = -((radius**2-y**2)**.5)
        elif c < .4125: y = (radius**2-x**2)**.5
        else: y = -((radius**2-x**2)**.5)
        x, y = random.random()*.01+x, random.random()*.01+y
    n = x**2+y**2
    if sign == "<": n = float(n<radius**2)
    elif sign == ">": n = float(n>radius**2)
    elif sign == "<=": n = float(n<=radius**2)
    elif sign == ">=": n = float(n>=radius**2)
    invals.append( [x, y, 1.0] )
    i_use.append( [x, y, 1.0] )
    answers.append(n)
weights = [[[random.uniform(-1,1) for a in range(layercts[0])] for b in range(layercts[1])], [[random.uniform(-1,1) for a in range(layercts[1])] for a in range(layercts[2])], [[random.uniform(-1,1) for a in range(layercts[2])] for a in range(layercts[3])], [[random.uniform(-1,1) for a in range(layercts[3])] for a in range(layercts[4])]]
w_use = []
for data in weights: 
    w_use.append( [] )
    for elem in data:
        w_use[-1].append( [num for num in elem] )

def backprop(err, err_weights, xvals, err_nodes, weights):
    err_nodes[-1][-1] = err
    answer = 0.0
    for data in weights: 
        err_weights.append( [] )
        for elem in data:
            err_weights[-1].append( [0] * len(elem) )
    for i in range(len(err_nodes)):
        ii = -i-1
        for j in range(len(err_nodes[ii])):
            if not (i or j): continue
            err_nodes[ii][j] = xvals[ii][j] * (1.0-xvals[ii][j]) * err_nodes[ii+1][0] * weights[ii+1][0][j]
    for i in range(len(weights)):
        ii = -i-1
        for j in range(len(weights[ii])):
            for k in range(len(weights[ii][j])):
                err_weights[ii][j][k] = err_nodes[ii][j] * xvals[ii-1][k]
    return err_weights

def apply():
    xvals, yvals, final, ans = [], [], [], []
    while i_use:
        temp = i_use.pop(0)
        xvals.append( [] )
        yvals.append( [] )
        while w_use:
            pound, newtemp, x = w_use.pop(0), [], 0.0
            xvals[len(invals)-len(i_use)-1].append( [val for val in temp] )
            for y in range(len(pound)):
                x = 0
                for z in range(len(temp)): x += temp[z]*pound[y][z]
                newtemp.append(x)
            yvals[len(invals)-len(i_use)-1].append( [val for val in newtemp] )
            if w_use: temp = [1.0/(1.0+math.exp(-val)) for val in newtemp]
            else: temp = [val for val in newtemp]
        xvals[len(invals)-len(i_use)-1].append( [val for val in temp] )
        err = answers[len(invals)-len(i_use)-1]-temp[0]
        final.append(err)
        ans.append(temp[0])
        change = backprop(err, [], xvals[-1], [[0 for a in b] for b in xvals[-1][1:]], weights)
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                for k in range(len(weights[i][j])):
                    weights[i][j][k] += alpha * change[i][j][k]
        for data in weights: w_use.append( [elem for elem in data] )
    xvals, yvals = [], []
    for data in invals: i_use.append( [elem for elem in data] )
    return final, ans

bestweights = []
print("\nLayer cts:", layercts)
for data in weights: bestweights.append( [elem for elem in data] )
while time.time()-startTime < 99.5:
    err, ans = apply()
    errsum = sum(abs(sel) for sel in err)
    if errsum < minerrsum:
        minerrsum = errsum
        bestweights = []
        for data in weights: bestweights.append( [elem for elem in data] )
print("Weights:")
print(bestweights, sep='\n')
for i in range(len(bestweights)):
    temp = []
    for elem in bestweights[i]: temp += elem
    print(temp)
minerrsum = errsum