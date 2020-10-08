import random
import requests
import time
import math

population_size = 10  # Normalmente mayor, tipo 100
chromosome_size = 64  # Tamano del cromosoma 64 = 4 estaciones * 16 sensores/estacion
debug_level = 0
percentage_tournament = 0.5  # Con poblaciones de 100 suele ser un 2%-5% depende

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

def tournament_selection(population_fitness):
    # ------------------------------------------
    # Step 3: This method selects best individuals in the population using tournament
    # ------------------------------------------    
    t_size = math.floor(percentage_tournament * population_size)

    if debug_level >= 1:
        print("Tamaño torneo: " + str(t_size))

    selected = random.sample(range(population_size), t_size)

    if debug_level >= 1:
        for y in selected:
            # Select lower or best individual
            # Append best into new population
            print("Tournament participants: " + str(y) + " " + str(population_fitness[y]))

    return selected


population = step1_initialization()
population_fitness = evaluate_population(population)

if debug_level >= 1:
    print(population_fitness)
    print("Primer individuo poblacion: " + str(population[0]))
    print("Primer individuo poblacion: " + str(population[population_size-1]))
    print("Tamaño poblacion: " + str(len(population)))
    print("Tamaño cromosoma: " + str(len(population[0][0])))


selected = tournament_selection(population_fitness)
print("Selected individuals in tournament: ", selected)
