import random

import simpy

RANDOM_SEED = 42
NEW_PROCESS = 5
INTERVAL_PROCESS = 10.0

def source(env, number, interva, RAM, CPU, WAITING):

    for i in range(number):
        instrucciones = random.randint(1,10)
        memoria = random.randint(1,10)
        c = proceso(env, 'ID%03d' & i, memoria, RAM,CPU, WAITING, instrucciones)
        env.process(c)
        t = random.expovariate(1.0/ interval)
        yield env.timeout(t)

def proceso(env, processID, memoria, RAM, CPU, WAITING,instrucciones):
    arrive = env.now
    print '%7.4f %s: NEW (esperando RAM %s), RAM disponible %s' % (arrive, proce
    


        
