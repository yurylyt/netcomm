from numpy import random as rg

def trial(p):
    return rg.choice([True, False], p=[p, 1 - p])
