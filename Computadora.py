#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Universidad del Valle de Guatemala
# Algoritmos y Estructuras de Datos
# Seccion 30
# Esteban Barrera 13413
# Henry Orellana 13048
# Proposito del programa: Simula el funcionamiento de un sistema operativo.
# Referencia: ejemplo3.py que se presento en clase.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

# Se importan las distintas bibliotecas de python. Random y Simpy para la simulacion.
import random

import simpy

# Se definen las variables iniciales para ejecutar los distintos procesos del programa.
RANDOM_SEED = 42
NEW_PROCESS = 25
INTERVAL_PROCESS = 10.0

# Funcion "source": genera procesos con ciertos parametros que requiere los distintos
# procesos del sistema operativo.
def source(env, number, interval, RAM, CPU, WAITING):
    for i in range(number):
        instrucciones = random.randint(1,10) # Produce aleatoriamente las instrucciones
        memoria = random.randint(1,10) # Produce aleatoriamente los espacios para los procesos.
        c = proceso(env, 'ID%02d' % i, memoria, RAM,CPU, WAITING, instrucciones)
        env.process(c)
        t = random.expovariate(1.0/ interval)
        yield env.timeout(t)

# Funcion "proceso": realiza las distintas etapas y luego termina de ejecutar las instrucciones.
def proceso(env, processID, memoria, RAM, CPU, WAITING,instrucciones):
    global sumatoria
    global promedio
    global n
    arrive = env.now
    print ('%7.4f %s: NEW (esperando RAM %s), RAM disponible %s' % (arrive, processID, memoria, RAM.level))

    # Se encuentra en NEW y se necesita memoria para seguir a READY
    with RAM.get(memoria) as req:
        yield req #Esperar por memoria RAM

        wait = env.now - arrive
        print ('%7.4f %s: READY espero RAM %6.3f' % (env.now, processID, wait))

        # se lleva a cabo el proceso mientras tenga instrucciones por ejecutar.
        while instrucciones > 0:

            #Se encuentra en READY. Se necesita que haya un CPU disponible.
            with CPU.request() as reqCPU:   # Se espera a un CPU

                yield reqCPU
                print ('%7.4f %s: RUNNING instrucciones %6.3f' %(env.now, processID, instrucciones))

                yield env.timeout(1) # El tiempo que se dedica al CPU
                
            # Al finalizar el tiempo por el CPU se disminuye las instrucciones
            # que falta por hacer.
                if instrucciones > 3:
                    instrucciones = instrucciones - 3

                else:
                    instrucciones = 0

            # Tiempo terminado del proceso realizado por el CPU
            if instrucciones > 0:
                siguiente = random.choice(["ready", "waiting"])
                if siguiente == "waiting":
                    with WAITING.request() as reqWAITING:
                        yield reqWAITING
                        print ('%7.4f %s: WAITING' % (env.now,processID))

                        yield env.timeout(1)


                print ('%7.4f %s: READY' % (env.now, processID))

        # Proceso terminado.
        tiempoProceso = env.now - arrive
        print ('%7.4f %s: TERMINATED tiempo de ejecucion %s' % (env.now, processID,tiempoProceso))

        sumatoria = sumatoria + tiempoProceso
        n = n + 1
        with RAM.put(memoria) as reqDevolverRAM:
            yield reqDevolverRAM
            print ('%7.4f %s: Regresando RAM %s' % (env.now, processID, memoria))

# Se configura y empieza la simulacion del sistema operativo
print ('Sistema Operativo')
random.seed(RANDOM_SEED)
env = simpy.Environment()
sumatoria = 0
n = 0
# Inicia los procesos y los corre.
CPU = simpy.Resource(env, capacity=1)
RAM = simpy.Container(env, init = 100, capacity=100)
WAITING = simpy.Resource(env, capacity=1)
env.process(source(env,NEW_PROCESS, INTERVAL_PROCESS, RAM, CPU, WAITING))
env.run()
promedio = sumatoria/n
print ('Tiempo total en ejecutarse: ',sumatoria, 'Promedio: ',(promedio))
