def sum67(nums):
    l = []
    for i, n in enumerate(nums):
        print(i, n)
        l.append((0 if(n == 6) else 0 if (6 in nums[:i] and 7 not in nums[:i]) else 0 if(6 in nums[:i] and (nums[:i][-1].index(6) < nums[:i][-1].index(7))) else n))
        print(l)
    return sum(l)

sum67([6, 7, 1, 6, 7, 7])