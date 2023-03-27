from evotools import *
from evotraits import *

# class defining an evolution environment
class Environment:
    class EnvObject:
        def __init__(self, x, y, canwin):
            self.x = x
            self.y = y
            self.canwin = canwin
            self.rank = -1
            self.ranker = None
            self.score = 0
            self.stack = 0
            self.dir = rng.integers(4)
        def behavior(self, env):
            pass
        def on_attacked(self, attacker, env):
            pass
        def mutate(self, env):
            pass
        
    class FoodObject(EnvObject):
        def __init__(self, x, y):
            super().__init__(x, y, False)
        def on_attacked(self, attacker, env):
            attacker.score+=1
            env.remove_obj(self)
    
    def __init__(self, size, winfunc, ranker, reverse_ranking=False, objects=[]):
        self.tiles = np.empty(shape=size, dtype=Environment.EnvObject) # tile grid
        self.size = size # size of environment
        self.winfunc = winfunc # Individual, Environment -> bool | chooses whether Individual can reproduce
        self.objects = [] # objects in environment
        self.ranker = ranker
        self.reverse_ranking = reverse_ranking
        self.successful = []
        self.time = 0
        self.generations = 0
        self.redundant_gens = 0
        if(objects != []):
            for obj in objects:
                self.insert_obj(obj)
            
    def reset(self):
        self.tiles = np.empty(shape=self.size, dtype=Environment.EnvObject)
        self.objects = []
    
    def insert_obj(self, obj):
        if(obj.canwin): 
            obj.ranker = self.ranker
            self.objects.append(obj)
        self.tiles[obj.x, obj.y] = obj
        
    def remove_obj(self, obj):
        self.tiles[obj.x, obj.y] = None
        if(obj.canwin):
            self.objects.remove(obj)
        del obj
        
    def populate_area_random(self, n, w, h, num_genes=default_rnd_genes, lf=0, tp=0):
        i=0
        while i < n:
            x = np.random.randint(lf, lf+w)
            y = np.random.randint(tp, tp+h)
            if(self.tiles[x,y] != None):
                continue
            
            indi = Individual(generate_rnd_genome(num_genes), x, y)
            self.insert_obj(indi)
            i+=1
            
    def place_food_random(self, n, w, h, lf=0, tp=0):
        i = 0
        while i < n:
            x = np.random.randint(lf, lf+w)
            y = np.random.randint(tp, tp+h)
            if(self.tiles[x,y] != None):
                continue
            
            indi = self.FoodObject(x, y)
            self.insert_obj(indi)
            i+=1
    
    def run(self):
        for o in self.objects:
            o.behavior(self)
        self.time+=1
    
    def try_mutations(self, p=.05):
        for o in self.objects:
            o.mutate(p)
        
    def get_successful(self):
        return list(filter(lambda o: self.winfunc(o, self), 
                           filter(lambda o: o.canwin, self.objects)))
    
    def ranksort(self):
        return sorted(filter(lambda p: p.rank != -1, self.get_successful()), 
                      key=lambda p: p.rank, reverse=self.reverse_ranking)
    
    def repopulate(self, n, w, h, lf=0, tp=0, num_genes=default_rnd_genes):
        successful = self.ranksort()
        self.reset()
        i=0
        count = len(successful)
        if(count == 0):
            self.redundant_gens+=1
            successful = self.successful
            count = len(successful)
        dist = None
        if(count > 1):
            self.successful = successful
            dist = [zipf_pmf(count, i) for i in range(1, count+1)]
            dist = [p + (1-sum(dist))/count for p in dist]
        while i < n:
            x = np.random.randint(lf, lf+w)
            y = np.random.randint(tp, tp+h)
            if(self.tiles[x,y] != None):
                continue
            
            genes = []
            if count == 0:
                genes = generate_rnd_genome(num_genes)
            elif count == 1:
                genes = successful[0].genes
            else:
                genes = rng.choice(successful[:count], p=dist).genes
            ind = Individual(genes, x, y)
            self.insert_obj(ind)
            i+=1
            
    def repopulate_from_genes(self, genes, n, w, h, dist=None, lf=0, tp=0):
        self.reset()
        i=0
        count = len(genes)
        if(count > 1 and dist == None):
            dist = [zipf_pmf(count, i) for i in range(1, count+1)]
            dist = [p + (1-sum(dist))/count for p in dist]
        while i < n:
            x = np.random.randint(lf, lf+w)
            y = np.random.randint(tp, tp+h)
            if(self.tiles[x,y] != None):
                continue
            
            g = []
            if count == 0:
                g = generate_rnd_genome(default_rnd_genes)
            elif count == 1:
                g = genes[0]
            else:
                g = rng.choice(genes, p=dist)
            ind = Individual(g, x, y)
            self.insert_obj(ind)
            i+=1
    
    def generation(self, frames, sidechain=nop, post=nop, p=.05, 
                   repop=0, repopw=0, repoph=0, rplf=0, rptp=0):
        '''
        Run the environment then allow winning bacteria to reproduce with mutation.
        
        int frames: number of frames to run for before reproduction
        function sidechain: function that runs after every frame
        function post: function that runs after generation
        float p: probability of mutation
        int repop: number of children to repopulate
        int repopw, repoph, rplf, rptp: width, height, left, top of simulation             
        '''
        for i in range(frames):
            sidechain()
            self.run()
        sidechain()
        
        self.repopulate(repop, repopw, repoph, rplf, rptp)
        self.try_mutations(p)
        self.time = 0
        post()
        self.generations+=1
        
    def outofbounds(self, x, y):
        return not (x >= 0 and x < self.size[0] and y >= 0 and y < self.size[1])
    def emptyTile(self, x, y):
        if not self.outofbounds(x, y):
            return self.tiles[x,y] == None
        return True
    def isFood(self, x, y):
        if not self.emptyTile(x, y):
            return isinstance(self.tiles[x, y], Environment.FoodObject)
        return False
    
# class defining an individual in the simulation with a certain genome
class Individual(Environment.EnvObject):
    def __init__(self, genes, x, y):
        super().__init__(x, y, True)
        self.genes = genes # list of sense id : behavior id tuples

    def behavior(self, env):
        for (s, b) in self.genes:
            # for each activated sense, perform behavior connected to it
            if(senses[s](self, env)):
                behaviors[b](self, env)
        if(env.winfunc(self, env)):
            self.rank = self.ranker(self, env)
    
    def on_attacked(self, attacker, env):
        pass
    
    # mutates genes with mutation probability p
    def mutate(self, p):
        if(rng.random() < p):
            i = rng.choice(range(len(self.genes)))
            choice = rng.choice((0,1))
            if(choice == 0):
                self.genes[i] = (rng.integers(len(senses)), self.genes[i][1])
            else:
                self.genes[i] = (self.genes[i][0], rng.integers(len(behaviors)))