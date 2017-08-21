import sys
from collections import deque
from functools import reduce
from mapping_periods import lcm

def list_lcm(l):
    if l:
        return reduce(lcm, l)
    else:
        return 1

def prime_sieve(n):
    l = [2]
    for x in range(3, n + 1):
        if not any(x % i == 0 for i in l):
            l.append(x)
    return l

def find_lcms(max_sum, l=[]):
    curr_lcm = list_lcm(l)
    curr_sum = sum(l)
    for i in range(1, max_sum):
        if curr_sum + i > max_sum:
            yield l.copy(), curr_lcm
            break
        elif curr_lcm % i != 0:
            l.append(i)
            yield from find_lcms(max_sum, l)
            l.pop(-1)

def find_highest_lcm(max_sum):
    highest = 0
    best_l = None
    for a, b in find_lcms(max_sum):
        if b > highest:
            best_l = a
            highest = b
    return best_l, highest

print(find_highest_lcm(int(sys.argv[1])))
