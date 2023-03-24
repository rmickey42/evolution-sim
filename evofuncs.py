from evoenvironment import *

sight_range = 8

# 0: simple tick sense that activates every frame
def tick(obj, env):
    return True

# 1: sense of something above
def snup(obj, env):
    return not (env.emptyTile(obj.x, obj.y-1))

# 2: sense of something below
def sndw(obj, env):
    return not (env.emptyTile(obj.x, obj.y+1))

# 3: sense of something to the left
def snlf(obj, env):
    return not (env.emptyTile(obj.x-1, obj.y))

# 4: sense of something to the right
def snri(obj, env):
    return not (env.emptyTile(obj.x+1, obj.y))

# 5: sense of food above
def snfdup(obj, env):
    lo, hi = 0, 0
    for i in range(1, sight_range+1):
        for j in range(lo, hi+1):
            if env.isFood(obj.x+j, obj.y-i):
                return True
        lo-=1
        hi+=1
    return False
        
# 6: sense of food below
def snfddn(obj, env):
    lo, hi = 0, 0
    for i in range(1, sight_range+1):
        for j in range(lo, hi+1):
            if env.isFood(obj.x+j, obj.y+i):
                return True
        lo-=1
        hi+=1
    return False

# 7: sense of food to left
def snfdlf(obj, env):
    lo, hi = 0, 0
    for i in range(1, sight_range+1):
        for j in range(lo, hi+1):
            if env.isFood(obj.x-i, obj.y+j):
                return True
        lo-=1
        hi+=1
    return False

# 8: sense of food to right
def snfdri(obj, env):
    lo, hi = 0, 0
    for i in range(1, sight_range+1):
        for j in range(lo, hi+1):
            if env.isFood(obj.x+i, obj.y+j):
                return True
        lo-=1
        hi+=1
    return False

# 9: stack == 0
def sneqz(obj, env):
    return obj.stack == 0

# 10: stack < 0
def sngtz(obj, env):
    return obj.stack > 0

# 11: stack > 0
def snltz(obj, env):
    return obj.stack < 0

# create complement function
def notsn(sn):
    return lambda obj, env: not sn(obj, env)

# list containing boolean sensory functions for each sense ID, as well as their complements
senses = [tick, snup, sndw, snlf, snri, snfdup, snfddn, snfdlf, snfdri, sneqz, sngtz, snltz]
senses = senses + list(map(lambda sn: notsn(sn), senses))

# 0: try move up
def mvup(obj, env):
    if(env.emptyTile(obj.x, obj.y-1) and not env.outofbounds(obj.x, obj.y-1)):
        env.tiles[obj.x, obj.y-1] = obj
        env.tiles[obj.x, obj.y] = None
        obj.y-=1

# 1: try move down
def mvdn(obj, env):
    if(env.emptyTile(obj.x, obj.y+1) and not env.outofbounds(obj.x, obj.y+1)):
        env.tiles[obj.x, obj.y+1] = obj
        env.tiles[obj.x, obj.y] = None
        obj.y+=1

# 2: try move left
def mvlf(obj, env):
    if(env.emptyTile(obj.x-1, obj.y) and not env.outofbounds(obj.x-1, obj.y)):
        env.tiles[obj.x-1, obj.y] = obj
        env.tiles[obj.x, obj.y] = None
        obj.x-=1

# 3: try move right
def mvri(obj, env):
    if(env.emptyTile(obj.x+1, obj.y) and not env.outofbounds(obj.x+1, obj.y)):
        env.tiles[obj.x+1, obj.y] = obj
        env.tiles[obj.x, obj.y] = None
        obj.x+=1


# 4: attack/eat
def attack(obj, env):
    if(not env.emptyTile(obj.x, obj.y-1) and not env.outofbounds(obj.x, obj.y-1)):
        env.tiles[obj.x, obj.y-1].on_attacked(obj, env)
    if(not env.emptyTile(obj.x, obj.y+1) and not env.outofbounds(obj.x, obj.y+1)):
        env.tiles[obj.x, obj.y+1].on_attacked(obj, env)
    if(not env.emptyTile(obj.x-1, obj.y) and not env.outofbounds(obj.x-1, obj.y)):
        env.tiles[obj.x-1, obj.y].on_attacked(obj, env)
    if(not env.emptyTile(obj.x+1, obj.y) and not env.outofbounds(obj.x+1, obj.y)):
        env.tiles[obj.x+1, obj.y].on_attacked(obj, env)
        
#  6: increment stack
def incstack(obj, env):
    obj.stack+=1

# 7: decrement stack
def decstack(obj, env):
    obj.stack-=1

behaviors = [mvup, mvdn, mvlf, mvri, attack, incstack, decstack] # list containing behavior functions for each behavior ID

def generate_rnd_genome(num_genes):
    genes = []
    for i in range(num_genes):
        sense = rng.integers(len(senses))
        behavior = rng.integers(len(behaviors))
        genes.append((sense, behavior))
    return genes
