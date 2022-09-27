import sys
import math

num = int(sys.argv[1])
LOOKUP = [0, 1]

def fibonacci(x):
    while x >= len(LOOKUP):
        LOOKUP.append(LOOKUP[-1]+LOOKUP[-2])
    return LOOKUP[x]

print(fibonacci(num))