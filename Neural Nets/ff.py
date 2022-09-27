import math, time, sys, random, re

filename = sys.argv[1]
function = sys.argv[2]
inputs = [float(x) for x in sys.argv[3:]]

def process(a):
    if function == "T1" or function == "T2" and a > 0: return a
    if function == "T2": return 0.0
    if function == "T3": return 1.0/(1.0+math.exp(-a))
    if function == "T4": return 2.0/(1.0+math.exp(-a))-1.0
    return math.inf

weights = []
lines = open(filename, 'r')
for line in lines: weights.append( [float(x.rstrip()) for x in line.split(' ')] )

while len(weights):
    new_inputs = []
    nodes = len(weights[0])//len(inputs)
    if len(weights)-1:
        for i in range(nodes): new_inputs.append( process(sum([inputs[j] * weights[0][j+i*len(inputs)] for j in range(len(inputs))])) )
    else:
        for j in range(len(inputs)): new_inputs.append( inputs[j] * weights[0][j] )
    weights = weights[1:]
    inputs = new_inputs

print(*inputs)