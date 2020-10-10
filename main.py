import random
import requests
import time
import math
import matplotlib.pyplot as plt
import csv
# import functools

population_size = 100  # Normalmente mayor, tipo 100
chromosome_size = 64  # Tamano del cromosoma 64 = 4 estaciones * 16 sensores/estacion
debug_level = 0
percentage_tournament = 0.05  # Con poblaciones de 100 suele ser un 2%-5% depende
percentage_mutation = 0.05

PLOTTING_REAL_TIME = 1  # Choose to show fitness plot in real time

def step1_initialization():
    # ------------------------------------------
    # Step 1: Uniform random initialization of all genes/bits
    # ------------------------------------------
    population = []
    for x in range(population_size):
        population.append([])
        chromosome_partial = ''
        for y in range(chromosome_size):
            randInt = random.randint(0, 1)
            chromosome_partial = chromosome_partial + str(randInt)
        population[x].append(chromosome_partial)
    return population

# @functools.lru_cache(maxsize=128)
def get_individual_fitness(individual):
    # This is for getting the fitness of an specific individual
    url = "http://memento.evannai.inf.uc3m.es/age/test?c="
    url = url + str(individual[0])
    try:
        if debug_level >= 2:
            print(str(individual[0]))
        r = requests.get(url).content
    except:
        print("Exception when calling web service")
        time.sleep(1)
        r = requests.get(url).content
        # Podria hacer un bucle con un número máximo de intentos aquí para
        # evitar timeouts y problemas en la llamada al servicio web
    return float(r)


def evaluate_population(population):
    # ------------------------------------------
    # Step 2: This method evaluates a population
    # ------------------------------------------
    population_fitness = []
    # List with two elements: min fitness value and corresponding individual
    min_fitness = [float('inf'), None]
    for x in range(population_size):
        ind_fitness = get_individual_fitness(population[x])
        population_fitness.append(ind_fitness)
        if ind_fitness < min_fitness[0]:
            min_fitness[0] = ind_fitness
            min_fitness[1] = population[x][0]

    return population_fitness, min_fitness

def tournament_selection(population, population_fitness):
    # ------------------------------------------
    # Step 3: This method selects best individuals in the population using tournament
    # ------------------------------------------ 
    t_size = math.floor(percentage_tournament * population_size)

    new_population = []

    if debug_level >= 1:
        print("Tamaño torneo: " + str(t_size))

    for i in range(population_size):
        selected_index = random.sample(range(population_size), t_size)
        best_fitness_round = float('inf')
        winner = -1

        for y in selected_index:
            # Select lower or best individual
            if debug_level >=2 :
                print("Tournament participants: " + str(y) + " " + str(population_fitness[y]))             
            if population_fitness[y] < best_fitness_round:
                winner = y
                best_fitness_round = population_fitness[y]

        new_population.append(population[winner])   

    return new_population

def reproduction(population):
    # ------------------------------------------
    # Step 4: Reproduction among individuals in population
    # ------------------------------------------ 
    new_population = []
    for i in range(0,population_size,2):
        padre = population[i][0]
        madre = population[i+1][0]
        son1 = ''
        son2 = ''

        for j in range(chromosome_size):
            rand1 = random.random()
            rand2 = random.random()
            # primer son
            if (rand1 > 0.5):
                son1 = son1 + padre[j]
            else:
                son1 = son1 + madre[j]
            # second son
            if (rand2 > 0.5):
                son2 = son2 + padre[j]
            else:
                son2 = son2 + madre[j]
        
        new_population.append([son1])
        new_population.append([son2])

    return new_population

def mutation(population):
    # ------------------------------------------
    # Step 5: Mutation of individuals given a mutation percentage
    # ------------------------------------------ 
    for i in range(population_size):
        rand = random.random()
        if rand < percentage_mutation:
            randPos = random.randint(0, chromosome_size-1)
            
            if debug_level > 2:
                print("MUTATION in position ",randPos)
                print("before ",population[i])
            
            num = population[i][0][randPos]
            individual = list(population[i][0])

            if 0 == int(num):
                individual[randPos] = '1'
            else: 
                individual[randPos] = '0'

            population[i][0] = "".join(individual)

            if debug_level > 2:
                print("after  ",population[i])

    return population


### Main() ###

generations_plt = []
fitness_curve = []

# Population initialization
population = step1_initialization()

# CSV file for storing best generation individual
with open('best_fitness.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(['PARAMETERS used:'])
    wr.writerow([' - ELITISM', 'FALSE'])
    wr.writerow([' - GENERATIONAL', 'TRUE'])
    wr.writerow([' - Population size', population_size])
    wr.writerow([' - Tournament (%)', percentage_tournament])
    wr.writerow([' - Mutation rate (%)', percentage_mutation])
    wr.writerow(['--------------'])
    wr.writerow(['Fitness_value','Individual'])

    for i in range(0,100):
        print("--- Generation ", i," ---")
        generations_plt.append(i)

        # Evaluate population and get best individual
        population_fitness, min_fitness = evaluate_population(population)
        fitness_curve.append(min_fitness[0])

        # CSV write best individual value
        wr.writerow(min_fitness)
        
        # Plot best individual
        if PLOTTING_REAL_TIME == 1:
            plt.plot(generations_plt, fitness_curve, 'b', linewidth=1.0, label='Best individual fitness')
            if i==0:
                plt.legend()
                plt.xlabel('Generations')
                plt.ylabel('Fitness')
            plt.pause(0.05)
        
        # Stopping condition
        if (min_fitness[0] < 5):
            plt.savefig('fitness_value.png')
            wr.writerow(['TOTAL GENERATIONS: ', i+1])
            break

        if debug_level >= 1:
            print(population_fitness)
            print("Primer individuo poblacion: " + str(population[0]))
            print("Primer individuo poblacion: " + str(population[population_size-1]))
            print("Tamaño poblacion: " + str(len(population)))
            print("Tamaño cromosoma: " + str(len(population[0][0])))

        new_population = tournament_selection(population, population_fitness)
        # print(new_population)
        population_sons = reproduction(new_population)
        # print(population_sons)
        population = mutation(population_sons)
        # print(population)