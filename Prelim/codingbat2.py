def string_times(str, n):
    return str*n
def front_times(str, n):
    return str[:min(len(str), 3)]*n
def string_bits(str):
    return str[::2]
def string_splosion(str):
    return ''.join([str[:x] for x in range(len(str)+1)])
def last2(str):
    return sum([1 for x in range(len(str)-2) if str[x:x+2] == str[-2:]])
def array_count9(nums):
    return sum([1 for x in nums if x == 9])
def array_front9(nums):
    return 9 in nums and len(nums) < 4 or 9 in nums[:4]
def array123(nums):
    return True in [nums[x]==1 and nums[x+1]==2 and nums[x+2]==3 for x in range(len(nums)-2)]
def string_match(a, b):
    return sum([1 for x in range(min(len(a), len(b))-1) if a[x:x+2] == b[x:x+2]])
def double_char(str):
    return ''.join(str[a]*2 for a in range(len(str)))
def count_hi(str):
    return len(str.split('hi'))-1
def cat_dog(str):
    return len(str.split('dog'))-1 == len(str.split('cat'))-1
def count_code(str):
    return sum([1 for x in range(0, len(str)-3) if str[x:x+2] == 'co' and str[x+3] == 'e'])
def end_other(a, b):
    return b.lower().endswith(a.lower()) or a.lower().endswith(b.lower())
def xyz_there(str):
    return str.find('xyz') != -1 and (str[max(0, str.find('xyz')-1)] != '.' or xyz_there(str[str.find('xyz')+3:]))
def make_bricks(small, big, goal):
    return small + big*5 >= goal and goal%5 - small <= 0 
def lone_sum(a, b, c):
    return (a * (a != b and a != c)) + (b * (b != a and b != c)) + (c * (c != a and c != b))
def lucky_sum(a, b, c):
    return (a * (a != 13)) + (b * (a != 13 and b != 13)) + (c * (a != 13 and b != 13 and c != 13))
def no_teen_sum(a, b, c):
    return (a * (a not in [13, 14, 17, 18, 19])) + (b * (b not in [13, 14, 17, 18, 19])) + (c * (c not in [13, 14, 17, 18, 19]))
def round_sum(a, b, c):
    return ((((a-5)//10)+1)*10) + ((((b-5)//10)+1)*10) + ((((c-5)//10)+1)*10)
def close_far(a, b, c):
    return abs(a-b) <= 1 and abs(a-c) >= 2 and abs(b-c) >=2 or abs(a-b) >=2 and abs(a-c) <= 1 and abs(b-c) >= 2
def make_chocolate(small, big, goal):
    return ((goal-(big*5)<=small and goal%5<=small)*(max(goal-(big*5), goal%5)+1))-1
def count_evens(nums):
    return sum([abs(x%2-1) for x in nums])
def big_diff(nums):
    return max(nums)-min(nums)
def centered_average(nums):
    return int((sum(nums)-max(nums)-min(nums))/(len(nums)-2))
def sum13(nums):
    return sum([nums[a] for a in range(len(nums)) if nums[a] != 13 and (a == 0 or nums[a-1] != 13)])
def sum67(nums):
    return sum([(0 if(n == 6) else 0 if (6 in nums[:i] and 7 not in nums[:i]) else 0 if(6 in nums[:i] and (nums[:i][::-1].index(6) < nums[:i][::-1].index(7))) else n) for i, n in enumerate(nums)])
def has22(nums):
    return True in [nums[x]==2 and nums[x+1]==2 for x in range(len(nums)-1)]