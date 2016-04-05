from random import random
from math import floor, sqrt

def roll(base, interval):
    return floor(base + interval * random())

def calcLevel(xp):
    return floor(sqrt(xp / 1800.0))

def sgn(x):
    if x < 0:
        return -1
    else:
        return 1
    #return (x < 0 ? -1 : 1)

def any(x):
    if x > 0:
        return 1
    else:
        return 0
