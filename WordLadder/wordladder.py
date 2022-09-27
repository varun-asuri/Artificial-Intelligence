import time
import math
import sys

def ladder(filename):
    startTime = time.time()
    graph = {}
    f = open(filename, 'r')
    num = 0
    edge = 0
    con_com = []
    for raw in f:
        num = num + 1
        word = raw.rstrip()
        sims = []
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for a in range(len(alphabet)):
            for n in range(6):
                other = word[:n] + alphabet[a] + word[n+1:]
                if other in graph:
                    sims.append(other)
                    graph[other].append(word)
                    edge = edge + 2
        graph[word] = sims
    visited = set()
    for component in graph:
        if component in visited:
            continue
        else:
            archive = []
            parseMe = [component]
            while parseMe:
                copy = []
                for poss in parseMe:
                    if poss not in visited:
                        archive.append(poss)
                        visited.add(poss)
                    for x in graph[poss]:
                        if x not in visited:
                            copy.append(x)
                parseMe = copy
            con_com.append(archive)
    a = set([len(x) for x in con_com])
    degrees = [0]
    first = ''
    second = ''
    k2 = 0
    k3 = 0
    k4 = 0
    for wg in graph:
        length = len(graph[wg])
        if length >= len(degrees):
            second = first
            first = wg
        if length == len(degrees)-2:
            second = wg
        if length == 1 and len(graph[graph[wg][0]]) == 1:
            k2 = k2 + 1
        if length == 2 and len(graph[graph[wg][0]]) == 2 and len(graph[graph[wg][1]]) == 2 and graph[wg][0] in graph[graph[wg][1]]:
            k3 = k3 + 1
        if length == 3 and len(graph[graph[wg][0]]) == 3 and len(graph[graph[wg][1]]) == 3 and len(graph[graph[wg][2]]) == 3 and graph[wg][0] in graph[graph[wg][1]] and graph[wg][0] in graph[graph[wg][2]] and graph[wg][1] in graph[graph[wg][2]]:
            k4 = k4 + 1
        degrees = degrees + ([0] * max(0, length-len(degrees)+1))
        degrees[length] = degrees[length] + 1
    path = []
    farthest = ''
    if len(sys.argv) > 2:
        parseMe = [sys.argv[2]]
        dictionary = {sys.argv[2]:""}
        for word in parseMe:
            farthest = word
            if word == sys.argv[3]:
                b = []
                x = word
                while x != "":
                    b.append(x)
                    x = dictionary[x]
                path = b[::-1]
            b = graph[word]
            for x in b:
                if x not in dictionary:
                    parseMe.append(x)
                    dictionary[x] = word
    print()
    print('Word count: ' + str(num))
    print('Edge count: ' + str(edge/2)[:-2])
    print('Degree list: ', end='')
    print(*degrees, sep=' ')
    print('Construction time: ' + str(time.time()-startTime)[:4] + 's')
    print('Second degree word: ' + second)
    print('Connected component size count: ' + str(len(a)))
    print('Largest component size: ' + str(max(a)))
    print('K2 count: ' + str(k2/2)[:-2])
    print('K3 count: ' + str(k3/3)[:-2])
    print('K4 count: ' + str(k4/4)[:-2])
    if len(sys.argv) > 2:
        print('Neighbors: ', end='')
        print(*graph[sys.argv[2]], sep=' ')
    print('Farthest: ' + farthest)
    if len(sys.argv) > 2:
        print('Path: ', end='')
        print(*path, sep=' ')
    print("Time Used: " + str(time.time()-startTime)[:4])

ladder(sys.argv[1])