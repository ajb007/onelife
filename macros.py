from random import random
from math import floor

def roll(base, interval):
    return floor(base + interval * random())
