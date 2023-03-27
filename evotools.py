import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib as mpl
from IPython.display import display, HTML
import time

default_rnd_genes = 24
sight_range = 12
rng = np.random.default_rng()

def nop(*args, **kwargs):
    pass

zipfdic = {}
def zipf_pmf(x, n):
    """
    Calculate the value of the Zipf PMF at a given x for n categories.
    
    Parameters:
    x (int): The rank of the category.
    n (int): The total number of categories.
    
    Returns:
    float: The value of the Zipf PMF at the given rank x.
    """
    if(n in zipfdic):
        if(x in zipfdic[n]):
            return zipfdic[n][x]
    else:
        zipfdic[n] = {}
    
    # Calculate the normalization constant
    harmonic_sum = sum([1 / i for i in range(1, n+1)])
    c = 1 / harmonic_sum
    
    # Calculate the value of the Zipf PMF at rank x
    zipfdic[n][x] = c * (1 / x)
    
    return zipfdic[n][x]

# direction vectors for each ID: 0:right, 1:down, 2:left, 3:down 
# adding 1 = rotate right; subtract 1 = rotate left
directions = [ (1, 0), (0, 1), (-1, 0), (0, -1) ]

def perp(d):
    return d[1], d[0]

# v1 + v2
def addvec(x1, y1, x2, y2):
    return x1+x2, y1+y2

def addvec(v1, v2):
    return v1[0]+v2[0], v1[1]+v2[1]

# scal * v
def scalevec(scal, x, y):
    return scal*x, scal*y

def scalevec(scal, v):
    return scal*v[0], scal*v[1]