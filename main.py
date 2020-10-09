import random
import requests
import time
import math

population_size = 10  # Normalmente mayor, tipo 100
chromosome_size = 64  # Tamano del cromosoma 64 = 4 estaciones * 16 sensores/estacion
debug_level = 0
percentage_tournament = 0.5  # Con poblaciones de 100 suele ser un 2%-5% depende
percentage_mutation = 0.5

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
    for x in range(population_size):
        population_fitness.append(get_individual_fitness(population[x]))

    return population_fitness

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
        
        new_population.append(son1)
        new_population.append(son2)

    return new_population

def mutation(population):
    # ------------------------------------------
    # Step 5: Mutation of individuals given a mutation percentage
    # ------------------------------------------ 
    new_population = []
    for i in range(population_size):
        for j in range(chromosome_size):
            rand = random.random()
            if rand < percentage_mutation:
                print("MUTATION!")
                num = population[i][j]
                if 0 == int(num):
                    population[i][j] = population[i][:j] + '1' + population[i][j+2:]
                else: 
                    population[i][j] = population[i][:j] + '0' + population[i][j+2:]

    return new_population

population = step1_initialization()
population_fitness = evaluate_population(population)

if debug_level >= 1:
    print(population_fitness)
    print("Primer individuo poblacion: " + str(population[0]))
    print("Primer individuo poblacion: " + str(population[population_size-1]))
    print("Tamaño poblacion: " + str(len(population)))
    print("Tamaño cromosoma: " + str(len(population[0][0])))

new_population = tournament_selection(population, population_fitness)

population_sons = reproduction(new_population)
