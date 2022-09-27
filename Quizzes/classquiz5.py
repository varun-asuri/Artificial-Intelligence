import time
import math
import sys

def neighbors(puzzle):
    a = []
    for n in range(15):
        if puzzle[n] == '.':
            if n == 0:
                if puzzle[3] == '1' and puzzle[1] == '1':
                    a.append( ('1.' + puzzle[2] + '.' + puzzle[4:], '1/') )
                if puzzle[5] == '1' and puzzle[2] == '1':
                    a.append( ('1' + puzzle[1] + '.' + puzzle[3:5] + '.' + puzzle[6:], '2\\') )
            elif n == 1:
                if puzzle[6] == '1' and puzzle[3] == '1':
                    a.append( (puzzle[0] + '1' + puzzle[2] + '.' + puzzle[4:6] + '.' + puzzle[7:], '3/') )
                if puzzle[8] == '1' and puzzle[4] == '1':
                    a.append( (puzzle[0] + '1' + puzzle[2:4] + '.' + puzzle[5:8] + '.' + puzzle[9:], '4\\') )
            elif n == 2:
                if puzzle[7] == '1' and puzzle[4] == '1':
                    a.append( (puzzle[0:2] + '1' + puzzle[3] + '.' + puzzle[5:7] + '.' + puzzle[8:], '4/') )
                if puzzle[9] == '1' and puzzle[5] == '1':
                    a.append( (puzzle[0:2] + '1' + puzzle[3:5] + '.' + puzzle[6:9] + '.' + puzzle[10:], '5\\') )
            elif n == 3:
                if puzzle[0] == '1' and puzzle[1] == '1':
                    a.append( ('..' + puzzle[2] + '1' + puzzle[4:], '1/') )
                if puzzle[5] == '1' and puzzle[4] == '1':
                    a.append( (puzzle[0:3] + '1..' + puzzle[6:], '4-') )
                if puzzle[10] == '1' and puzzle[6] == '1':
                    a.append( (puzzle[0:3] + '1' + puzzle[4:6] + '.' + puzzle[7:10] + '.' + puzzle[11:], '6/') )
                if puzzle[12] == '1' and puzzle[7] == '1':
                    a.append( (puzzle[0:3] + '1' + puzzle[4:7] + '.' + puzzle[8:12] + '.' + puzzle[13:], '7\\') )
            elif n == 4:
                if puzzle[11] == '1' and puzzle[7] == '1':
                    a.append( (puzzle[0:4] + '1' + puzzle[5:7] + '.' + puzzle[8:11] + '.' + puzzle[12:], '7/') )
                if puzzle[13] == '1' and puzzle[8] == '1':
                    a.append( (puzzle[0:4] + '1' + puzzle[5:8] + '.' + puzzle[9:13] + '.' + puzzle[14], '8\\') )    
            elif n == 5:
                if puzzle[0] == '1' and puzzle[2] == '1':
                    a.append( ('.' + puzzle[1] + '.' + puzzle[3:5] + '1' + puzzle[6:], '2\\') )
                if puzzle[3] == '1' and puzzle[4] == '1':
                    a.append( (puzzle[0:3] + '..1' + puzzle[6:], '4-') )
                if puzzle[12] == '1' and puzzle[8] == '1':
                    a.append( (puzzle[0:5] + '1' + puzzle[6:8] + '.' + puzzle[9:12] + '.' + puzzle[13:], '8/') )
                if puzzle[14] == '1' and puzzle[9] == '1':
                    a.append( (puzzle[0:5] + '1' + puzzle[6:9] + '.' + puzzle[10:14] + '.', '9\\') )
            elif n == 6:
                if puzzle[1] == '1' and puzzle[3] == '1':
                    a.append( (puzzle[0] + '.' + puzzle[2] + '.' + puzzle[4:6] + '1' + puzzle[7:], '3/') )
                if puzzle[8] == '1' and puzzle[7] == '1':
                    a.append( (puzzle[0:6] + '1..' + puzzle[9:], '7-') )
            elif n == 7:
                if puzzle[2] == '1' and puzzle[4] == '1':
                    a.append( (puzzle[0:2] + '.' + puzzle[3:4] + '.' + puzzle[5:7] + '1' + puzzle[8:], '4/') )
                if puzzle[9] == '1' and puzzle[8] == '1':
                    a.append( (puzzle[0:7] + '1..' + puzzle[10:], '8-') )
            elif n == 8:
                if puzzle[1] == '1' and puzzle[4] == '1':
                    a.append( (puzzle[0] + '.' + puzzle[2:4] + '.' + puzzle[5:8] + '1' + puzzle[9:], '4\\') )
                if puzzle[6] == '1' and puzzle[7] == '1':
                    a.append( (puzzle[0:6] + '..1' + puzzle[9:], '7-') )
            elif n == 9:
                if puzzle[2] == '1' and puzzle[5] == '1':
                    a.append( (puzzle[0:2] + '.' + puzzle[3:5] + '.' + puzzle[6:9] + '1' + puzzle[10:], '5\\') )
                if puzzle[7] == '1' and puzzle[8] == '1':
                    a.append( (puzzle[0:7] + '..1' + puzzle[10:], '8-') )
            elif n == 10:
                if puzzle[3] == '1' and puzzle[6] == '1':
                    a.append( (puzzle[0:3] + '.' + puzzle[4:6] + '.' + puzzle[7:10] + '1' + puzzle[11:], '6/') )
                if puzzle[12] == '1' and puzzle[11] == '1':
                    a.append( (puzzle[0:10] + '1..' + puzzle[13:], '11-') )
            elif n == 11:
                if puzzle[4] == '1' and puzzle[7] == '1':
                    a.append( (puzzle[0:4] + '.' + puzzle[5:7] + '.' + puzzle[8:11] + '1' + puzzle[12:], '7/') )
                if puzzle[13] == '1' and puzzle[12] == '1':
                    a.append( (puzzle[0:11] + '1..' + puzzle[14:], '12-') )
            elif n == 12:
                if puzzle[3] == '1' and puzzle[7] == '1':
                    a.append( (puzzle[0:3] + '.' + puzzle[4:7] + '.' + puzzle[8:12] + '1' + puzzle[13:], '7\\') )
                if puzzle[5] == '1' and puzzle[8] == '1':
                    a.append( (puzzle[0:5] + '.' + puzzle[6:8] + '.' + puzzle[9:12] + '1' + puzzle[13:], '8/') )
                if puzzle[10] == '1' and puzzle[11] == '1':
                    a.append( (puzzle[0:10] + '..1' + puzzle[13:], '11-') )
                if puzzle[14] == '1' and puzzle[13] == '1':
                    a.append( (puzzle[0:12] + '1..', '13-') )
            elif n == 13:
                if puzzle[4] == '1' and puzzle[8] == '1':
                    a.append( (puzzle[0:4] + '.' + puzzle[5:8] + '.' + puzzle[9:13] + '1' + puzzle[14], '7/') )
                if puzzle[11] == '1' and puzzle[12] == '1':
                    a.append( (puzzle[0:11] + '..1' + puzzle[14:], '12-') )
            elif n == 14:
                if puzzle[5] == '1' and puzzle[9] == '1':
                    a.append( (puzzle[0:5] + '.' + puzzle[6:9] + '.' + puzzle[10:14] + '1', '9\\') )
                if puzzle[12] == '1' and puzzle[13] == '1':
                    a.append( (puzzle[0:12] + '..1', '13-') )
    return a

def solve(puzzle):
    parseMe = [(puzzle, 0)]
    dictionary = {puzzle: ("", 0)}
    n = puzzle.find('.')
    for puzzle, move in parseMe:
        if puzzle.count('1') == 1 and puzzle.find('1') == n:
            a = []
            x = (puzzle, move)
            while x[0] != "":
                a.append(x)
                x = dictionary[x[0]]
            a.append(x)
            a = a[::-1]
            for move in a[:-1]:
                print(move[1], end=' ')
            return ""
        a = neighbors(puzzle)
        for x, move in a:
            if x not in dictionary:
                parseMe.append((x, move))
                dictionary[x] = (puzzle, move)
    print('Unsolvable')
    print(puzzle)

solve(sys.argv[1])