from evotools import *
import evoenv
# note: commented indexes  and order are wrong; change later

# 0: dormant sense
def dormant(obj, env):
    return False

# sense food ahead radial
def snfdfw_r(obj, env):
    d = directions[obj.dir]
    p = perp(d)
    lo, hi = 0, 0
    for i in range(1, sight_range+1):
        for j in range(lo, hi+1):
            coords = addvec(scalevec(i, d), scalevec(j, p))
            if env.isFood(*addvec((obj.x, obj.y), coords)):
                return True
        lo-=1
        hi+=1
    return False

# sense food right radial
def snfdri_r(obj, env):
    d = directions[(obj.dir+1)%4]
    p = perp(d)
    lo, hi = 0, 0
    for i in range(1, sight_range+1):
        for j in range(lo, hi+1):
            coords = addvec(scalevec(i, d), scalevec(j, p))
            if env.isFood(*addvec((obj.x, obj.y), coords)):
                return True
        lo-=1
        hi+=1
    return False

# sense food left radial
def snfdlf_r(obj, env):
    d = directions[(obj.dir-1)%4]
    p = perp(d)
    lo, hi = 0, 0
    for i in range(1, sight_range+1):
        for j in range(lo, hi+1):
            coords = addvec(scalevec(i, d), scalevec(j, p))
            if env.isFood(*addvec((obj.x, obj.y), coords)):
                return True
        lo-=1
        hi+=1
    return False

# 10: stack == 0
def sneqz(obj, env):
    return obj.stack == 0

# 11: stack > 0
def sngtz(obj, env):
    return obj.stack > 0

# 12: stack < 0
def snltz(obj, env):
    return obj.stack < 0

# 17: stack <= neighbor ahead
def sncmpn(obj, env):
    tile = addvec((obj.x, obj.y), directions[obj.dir])
    if(not env.emptyTile(*tile) and not env.outofbounds(*tile)):
        return obj.stack <= env.tiles[tile].stack
    return False

# 13: wall ahead
def snwlfw(obj, env):
    return env.outofbounds(*addvec((obj.x, obj.y), directions[obj.dir]))

# 14: wall behind
def snwlbh(obj, env):
    return env.outofbounds(*addvec((obj.x, obj.y), directions[(obj.dir+2)%4]))

# 15: wall to left
def snwllf(obj, env):
    return env.outofbounds(*addvec((obj.x, obj.y), directions[(obj.dir-1)%4]))

# 16: wall to right
def snwlri(obj, env):
    return env.outofbounds(*addvec((obj.x, obj.y), directions[(obj.dir+1)%4]))

# 18: sense of individual ahead
def sninfw(obj, env):
    tile = addvec((obj.x, obj.y), directions[obj.dir])
    if not (env.emptyTile(*tile)):
        return isinstance(env.tiles[tile], evoenv.Individual)

# 19: sense of individual behind
def sninbh(obj, env):
    tile = addvec((obj.x, obj.y), directions[(obj.dir+2)%4])
    if not (env.emptyTile(*tile)):
        return isinstance(env.tiles[tile], evoenv.Individual)

# 20: sense of individual to the left
def sninlf(obj, env):
    tile = addvec((obj.x, obj.y), directions[(obj.dir-1)%4])
    if not (env.emptyTile(*tile)):
        return isinstance(env.tiles[tile], evoenv.Individual)

# 21: sense of individual to the right
def sninri(obj, env):
    tile = addvec((obj.x, obj.y), directions[(obj.dir+1)%4])
    if not (env.emptyTile(*tile)):
        return isinstance(env.tiles[tile], evoenv.Individual)
    
# 18: sense of food ahead
def snfdfw(obj, env):
    tile = addvec((obj.x, obj.y), directions[obj.dir])
    if not (env.emptyTile(*tile)):
        return isinstance(env.tiles[tile], evoenv.Environment.FoodObject)

# 19: sense of food behind
def snfdbh(obj, env):
    tile = addvec((obj.x, obj.y), directions[(obj.dir+2)%4])
    if not (env.emptyTile(*tile)):
        return isinstance(env.tiles[tile], evoenv.Environment.FoodObject)

# 20: sense of food to the left
def snfdlf(obj, env):
    tile = addvec((obj.x, obj.y), directions[(obj.dir-1)%4])
    if not (env.emptyTile(*tile)):
        return isinstance(env.tiles[tile], evoenv.Environment.FoodObject)

# 21: sense of food to the right
def snfdri(obj, env):
    tile = addvec((obj.x, obj.y), directions[(obj.dir+1)%4])
    if not (env.emptyTile(*tile)):
        return isinstance(env.tiles[tile], evoenv.Environment.FoodObject)

def notsn(sn):
    return lambda obj, env: not sn(obj, env)

# list containing boolean sensory functions for each sense ID
senses = [sneqz, sngtz, snltz, sncmpn,
          snwlfw, snwlbh, snwllf, snwlri, 
          snfdfw, snfdbh, snfdlf, snfdri,
          snfdfw_r, snfdlf_r, snfdri_r,
          sninfw, sninbh, sninlf, sninri]
senses = senses+list(map(notsn, senses))
senses.append(dormant)

# 0: try move ahead
def mvfw(obj, env):
    tile = addvec((obj.x, obj.y), directions[obj.dir])
    if(env.emptyTile(*tile) and not env.outofbounds(*tile)):
        env.tiles[tile] = obj
        env.tiles[obj.x, obj.y] = None
        obj.x = tile[0]
        obj.y = tile[1]

# 1: try move backward
def mvbk(obj, env):
    tile = addvec((obj.x, obj.y), directions[(obj.dir+2)%4])
    if(env.emptyTile(*tile) and not env.outofbounds(*tile)):
        env.tiles[tile] = obj
        env.tiles[obj.x, obj.y] = None
        obj.x = tile[0]
        obj.y = tile[1]

# 2: try move left
def mvlf(obj, env):    
    tile = addvec((obj.x, obj.y), directions[(obj.dir-1)%4])
    if(env.emptyTile(*tile) and not env.outofbounds(*tile)):
        env.tiles[tile] = obj
        env.tiles[obj.x, obj.y] = None
        obj.x = tile[0]
        obj.y = tile[1]

# 3: try move right
def mvri(obj, env):
    tile = addvec((obj.x, obj.y), directions[(obj.dir+1)%4])
    if(env.emptyTile(*tile) and not env.outofbounds(*tile)):
        env.tiles[tile] = obj
        env.tiles[obj.x, obj.y] = None
        obj.x = tile[0]
        obj.y = tile[1]


# 4: attack/eat ahead
def attack(obj, env):
    tile = addvec((obj.x, obj.y), directions[obj.dir])
    if(not env.emptyTile(*tile) and not env.outofbounds(*tile)):
        env.tiles[tile].on_attacked(obj, env)
        
# 5: increment stack
def incstack(obj, env):
    obj.stack+=1
    
# 6: decrement stack
def decstack(obj, env):
    obj.stack-=1
    
# 7: negate stack
def negstack(obj, env):
    obj.stack = -obj.stack
    
# 8: turn right
def tnri(obj, env):
    obj.dir = (obj.dir+1)%4

# 9: turn left
def tnlf(obj, env):
    obj.dir = (obj.dir-1)%4
    
# 10: turn around backwards
def tnbk(obj, env):
    obj.dir = (obj.dir+2)%4

# list containing behavior functions for each behavior ID
behaviors = [mvfw, mvbk, mvlf, mvri, attack, incstack, decstack, negstack, tnri, tnlf, tnbk]

def generate_rnd_genome(num_genes):
    genes = []
    for i in range(num_genes):
        sense = rng.integers(len(senses))
        behavior = rng.integers(len(behaviors))
        genes.append((sense, behavior))
    return genes