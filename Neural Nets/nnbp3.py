import math, time, sys, random, re

print()
filename, weights, weights, sqrcts, layercts, raw, cutoff = sys.argv[1], [], [], [1], [3, 1, 1], sys.argv[2][7:], 1
if raw[1] == '=': cutoff = 2
sign, radius = raw[:cutoff], float(raw[cutoff:])**.5
lines = open(filename, 'r')
for num, line in enumerate(lines):
    if any(char.isdigit() for char in line):
        sqrcts.append(1)
        newline = [x for x in line.rstrip().replace(',', '').split(' ') if any(char.isdigit() for char in x)]
        weights.append( [float(x) for x in newline]+[float(x) for x in newline] )
if sign[0] == '>': weights.append( [(1+math.e)/(2*math.e)] )
else: weights.append( [(1+math.e)/2] )
for i in range(-2, -len(sqrcts)-1, -1):
    sqrcts[i] = len(weights[i])//sqrcts[i+1]//2
for j in range(1, len(sqrcts)-1):
    layercts.insert(j, 2*sqrcts[j])
for a in range(len(weights)-1):
    count, top, split = 0, layercts[a]*layercts[a+1], layercts[a]//2
    for b in range(top):
        if a == 0:
            if top // (b+1) < 2 and count == 0: weights[a].insert(b, 0.0)
            elif top // (b+1) >= 2 and count == 1: weights[a].insert(b, 0.0)
            if count%3 != 2: weights[a][b] /= radius
            count = (count+1)%3
        elif a == len(weights)-2 and sign[0] == '<': weights[a][b] *= -1
        else:
            count += 1
            if count < 1: weights[a].insert(b, 0.0)
            if top // 2 == (b+1): count -= split
            elif count == split: count = -split
print("Inequality: x*x + y*y", sign, radius**2)
print("Layer cts:", layercts)
print("Weights:", *weights, sep='\n')