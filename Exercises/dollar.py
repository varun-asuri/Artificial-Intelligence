import sys
import math

sys.setrecursionlimit(1000000000)
num = int(sys.argv[1])
LOOKUP = [int(n) for n in sys.argv[2:]]
CURRENCY = {n: i for i, n in enumerate(LOOKUP)}
PASS_THROUGH = [0 for n in LOOKUP]
COMBINATIONS = []

def change(x, a):
    if not x:
        COMBINATIONS.append(a)
    else:
        for n, i in CURRENCY:
            if n <= x:
                a[i] += 1
                change(x-n, a)
                a[i] -= 1

change(num, PASS_THROUGH)
print(len(COMBINATIONS))
