import sys
s = ' '.join(sys.argv[1:]).replace('x', ' ').replace('X', ' ').replace('"', '').split(' ')
lst = [(int(s[i]), int(s[i+1])) for i in range(0,len(s),2)]