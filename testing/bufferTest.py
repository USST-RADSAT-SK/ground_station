import random
import matplotlib.pyplot as plt

"""
max size 5
start, end = dist

3, 0 = 2
stop o o start o

0, 0 = 0
start o o o o

0, 2 = 2
start o stop o o

3, 2 = 4
o o stop start o

2, 1 = 4
o stop start o o
"""

n = 5
start = 3
stop = 2

if start > stop:
    dist = n - start + stop
    print(dist == n - (start - stop))
elif start == stop:
    dist = 0
else:
    dist = stop - start

print(dist)