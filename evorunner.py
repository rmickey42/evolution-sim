from evoenv import Environment, nop
import sys, time, json

# environment with food condition
def foodWinfunc(food):
    return lambda ind, env: ind.score >= food

# run env for n generations
def run_n_generations(env, n, frames=100, repop=80, repopw=80, repoph=20, sidechain=nop, post=nop, p=.05, tp=0, lf=0):
    total = time.time()
    for i in range(n):
        t = time.time()
        env.generation(frames, sidechain=sidechain, repop=repop, repopw=repopw, repoph=repoph, rplf=lf, rptp=tp, post=post)
        print(f"Generation {i+1} complete (t={time.time()-t} s)")
    total = time.time()-total
    return total, total/n

total_food = 320
def foodplace():
    food_env.place_food_random(total_food, 80, 20, tp=60)

food_env = Environment((80,80), foodWinfunc(4), lambda ind,env: ind.score, True)

if(len(sys.argv) < 2):
    print(f"Usage: {sys.argv[0]} <generations> [load json]")
generations = int(sys.argv[1])
frames = 200
genes = []
if(len(sys.argv) >= 3):
    rfile = open(sys.argv[2])
    genes = json.load(rfile)
    rfile.close()

food_env.repopulate_from_genes(genes, 100, 80, 20, lf=0, tp=0)
foodplace()
total, avg = run_n_generations(food_env, generations, frames=frames, p=.15, post=foodplace, repop=100, repopw=80, repoph=20)
print("total time for " + str(generations) + " generations: " + str(total) + " | average generation time: " + str(avg))
print("saving successful genes to genes.json")
genestring = json.dumps(list(map(lambda s: s.genes, food_env.successful)))
wfile = open("genes.json")
wfile.write(genestring)
wfile.close()


    