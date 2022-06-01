import random
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint

from graph import GenerateGraph


# step 1
# creating initial population
def createInitialPopulation(graph, populationSize):
    population = []
    for i in range(0, populationSize):
        population.append(GenerateGraph.random_method(graph))  # dodać wybieranie pomiędzy random, k_random a two_optem
        # w dalszej części rozwoju programu dodać wyspy z populacjami
    # print("initial population: ", population)
    return population


# step 2
# evaluating and selection

# creating list of reversing costs of distance


def allFitness(graph, population):
    fitness = np.zeros(len(population))
    for i in range(0, len(population)):
        fitness[i] = graph.cost(population[i])  # upewnić się czy cost dodaje też koszt od ostatniego do pierwszego!

    for i in range(0, len(population)):
        if fitness[i] != 0:
            fitness[i] = 1 / fitness[i]

    # print("fitness ", fitness)
    return fitness


def sortRoutesByFitness(fitness):
    routes = list(range(0, len(fitness)))
    routesAndFitness = list(zip(routes, fitness))
    # przy obecnym sposobie selekcji niepotrzebne jest sortowanie jeśli
    # nie przenosimy elity w ruletce
    routesAndFitness.sort(key=lambda a: a[1], reverse=True)
    # print("sorted list ", routesAndFitness)

    return routesAndFitness


def roulette(routesRank, eliteSize):
    selection = []
    probabilityOfChoice = np.zeros(len(routesRank))
    sumOfFitness = sum(n for _, n in routesRank)
    # print("sumOfFitness ", sumOfFitness)
    for i in range(0, len(routesRank)):
        probabilityOfChoice[i] = 100 * routesRank[i][1] / sumOfFitness

    # sumOfProbabilty = 0
    # for i in range(0, len(probabilityOfChoice)):
    #     sumOfProbabilty += probabilityOfChoice[i]
    #
    # print("suma prawdopodobieństwa ", sumOfProbabilty)

    # print("probability ", probabilityOfChoice)
    # dzięki temu, że sortowaliśmy to tu przenosimy najlepszych
    # chosing elite - testować czy przydatne
    for i in range(0, eliteSize):
        selection.append(routesRank[i][0])

    for i in range(0, len(routesRank) - eliteSize):
        randomNumber = random.randrange(100)  # number in range(0-99)
        # print("randomNumber ", randomNumber)
        sumator = 0
        # czy należy ograniczyć wybieranie tych samych?
        for i in range(0, len(routesRank)):
            sumator += probabilityOfChoice[i]
            # print("sumator ", sumator)
            if randomNumber <= (sumator):  # sprawdzić wartości graniczne
                selection.append(routesRank[i][0])
                # print("add ", routesRank[i])
                sumator = 0
                break

    # print("routesRank size ", len(routesRank))
    # print("selection size", len(selection))

    return selection


def tournament(routesRank, k):
    contestant = randint(len(routesRank) - 1)
    for i in range(0, k):
        contestant2 = randint(len(routesRank) - 1)
        if routesRank[contestant2][1] < routesRank[contestant][1]:
            contestant = contestant2

    return routesRank[contestant][0]


def tournamentSelection(routesRank, eliteSize, k):
    selection = []
    for i in range(0, eliteSize):
        selection.append(routesRank[i][0])

    for i in range(0, len(routesRank) - eliteSize):
        selection.append(tournament(routesRank, k))
    return selection


def getParents(population, selectionIndexes):
    parents = []
    for i in range(0, len(selectionIndexes)):
        parents.append(population[selectionIndexes[i]])

    # print("parents ", parents)

    return parents


# def selection(Enum):
#     ROULETTE = roulette()
#     TOURNAMENT = tournament()

# step 3
# crossover
def orderCrossover(route1, route2):
    # print("parent1 ", route1)
    # print("parent2 ", route2)
    # print("dlugosc rodzica 1 ", len(route1))
    # zastanowić się czy generujemy 1 czy 2 dzieci
    children = []
    startSubstring = random.randint(1, (len(route1) - 3))
    # print("startSubstring ", startSubstring)
    endSubstring = random.randint(startSubstring + 1, (len(route1) - 2))  # sprawdzić dla wartości granicznych
    # print("endSubstring ", endSubstring)
    substring1 = route1[startSubstring:(endSubstring + 1)]
    # print("substring1 ", substring1)
    child1 = []
    child2 = []

    # generate child1
    numberOfAddedCities = 0
    l = 0
    while numberOfAddedCities < startSubstring and l < len(route2):
        if not route2[l] in substring1:
            child1.append(route2[l])
            numberOfAddedCities += 1
        l += 1
    # print("child1 ", child1)
    child1 = child1 + substring1
    # print("child1 after adding sub ", child1)
    for i in range(l, len(route2)):  # tu był błąd
        if not route2[i] in substring1:
            child1.append(route2[i])
    numberOfAddedCities = 0
    l = 0
    # print("child1 ", child1)
    # print("długosc dziecka ", len(child1))

    # generate child2
    # substring2 = route2[startSubstring:(endSubstring+1)]
    # print("substring2 ", substring2)
    # while numberOfAddedCities < startSubstring and l < len(route1):
    #         if not route1[l] in substring2:
    #             child2.append(route1[l])
    #             numberOfAddedCities += 1
    #             print("numberOfAddedCities ", numberOfAddedCities)
    #         l += 1
    # print("child2 ", child2)
    # print("l ", l)
    # child2 = child2 + substring2
    # for i in range(l + 1, len(route1)):
    #     if not route1[i] in substring2:
    #         child2.append(route1[i])
    # print("child2 ", child2)
    #
    # children = child1 + child2

    return child1


import random


def partiallyMappedCrossover(route1, route2):
    startSubstring = random.randint(1, (len(route1) - 3))
    # print("startSubstring ", startSubstring)
    endSubstring = random.randint(startSubstring + 1, (len(route1) - 2))  # sprawdzić dla wartości granicznych
    # print("endSubstring ", endSubstring)
    child1 = [0] * len(route1)
    replacement1 = [-1] * len(route1)

    for i in range(startSubstring, endSubstring + 1):
        child1[i] = route2[i]
        replacement1[route2[i]] = route1[i]

    # print("child1 ", child1)
    # print("replacement1 ", replacement1)
    # fill in remaining slots with replacements
    for i in range(0, len(route1)):
        if (i < startSubstring) or (i > endSubstring):
            n1 = route1[i]
            m1 = replacement1[n1]

            while m1 != -1:
                n1 = m1
                m1 = replacement1[m1]

            child1[i] = n1

    print("child1 ", child1)
    # print("replacement1 ", replacement1)

    return child1


# p1 = [2, 5, 1, 6, 4, 0, 8, 7, 3]
# p2 = [3, 1, 7, 5, 8, 4, 0, 6, 2]
# partiallyMappedCrossover(p1, p2)

def generateChildrenPopulation(graph, parents, eliteSize):
    children = []

    # adding elite from parent's population to children's population
    # czy tu też przenosić elitę?
    for i in range(0, eliteSize):
        children.append(parents[i])

    # guarantee that two different parents are selected
    numberOfGeneratedChildren = 0

    # pierwszy sposób wyboru rodziców do krzyżowania
    for i in range(0, len(parents) - 1):
        for j in range(i + 1, len(parents)):
            if numberOfGeneratedChildren == len(parents) - eliteSize:
                break
            elif parents[i] != parents[j]:
                children.append(orderCrossover(parents[i], parents[j]))
                # children.append(partiallyMappedCrossover(parents[i], parents[j]))
                numberOfGeneratedChildren += 1

    # drugi sposób wyboru rodziców do krzyżowania
    # for i in range(0, len(parents) - 1):
    #     if numberOfGeneratedChildren == len(parents) - eliteSize:
    #         break
    #     sample = 0
    #     while sample < 3:
    #         partner = random.randint(0, len(parents)-1)
    #         print("partner ", partner)
    #         if parents[i] != parents[partner]:
    #             children.append(orderCrossover(parents[i], parents[partner]))
    #             numberOfGeneratedChildren += 1
    #             sample = 0
    #             break
    #         sample += 1
    #     if sample == 3:
    #         children.append(parents[i])
    #         numberOfGeneratedChildren += 1

    if numberOfGeneratedChildren < (len(parents) - eliteSize):
        print("brakuje osobnikow: ", len(parents) - numberOfGeneratedChildren)
    # poniżej dopełnienie generacji dzieci generacją rodziców
    # ogromny wpływ na wyniki
    # parentIndex = len(parents) - 1
    # while numberOfGeneratedChildren < (len(parents) - eliteSize):
    #     children.append(parents[parentIndex])
    #     parentIndex -= 1
    #     numberOfGeneratedChildren += 1
    # poniżej drugi sposób dopełniania generacji dzieci
    # tutaj losowymiosobnikami, lepiej zabijać osobniki ktore często przechodzą
    while numberOfGeneratedChildren < (len(parents) - eliteSize):
        children.append(GenerateGraph.random_method(graph))
        numberOfGeneratedChildren += 1

    # if numberOfGeneratedChildren == 0:
    #     #print("only clones")
    #     children = [parents[0]]

    # print("children ", children)

    return children


# step 4
# mutation
# można również zaproponować mutację przez swaps lub naprawianie osobników dzięki 2-opt, ale o skróconym czasie działania
# prawdopodobieństwo mutacji powinno wynosić 1-5% (0.01 - 0.05)
def mutateByInvert(individual, mutationRate):
    new_individual = individual
    if (random.random() <= mutationRate):
        # print("mutation on ", individual)
        start = random.randint(0, len(individual) - 2)
        # print("start mutation index ", start)
        end = random.randint(start + 1, (len(individual) - 1))
        # print("end mutation index ", end)
        # new_individual = individual[:]
        new_individual[start:end + 1] = reversed(new_individual[start:end + 1])
        # print("individual after mutation ", new_individual)

    return new_individual


def mutateByTwoSwaps(individual, mutationRate):
    new_individual = individual
    if (random.random() <= mutationRate):
        # print("mutation on ", individual)
        start = random.randint(0, len(individual) - 2)
        # print("start mutation index ", start)
        end = random.randint(start + 1, (len(individual) - 1))
        # print("end mutation index ", end)
        # new_individual = individual[:]
        new_individual[start], new_individual[end] = new_individual[end], new_individual[start]
        # print("individual after mutation ", new_individual)
        start = random.randint(0, len(individual) - 2)
        # print("start mutation index ", start)
        end = random.randint(start + 1, (len(individual) - 1))
        # print("end mutation index ", end)
        # new_individual = individual[:]
        new_individual[start], new_individual[end] = new_individual[end], new_individual[start]

    return new_individual


def two_opt(graph, individual):
    path = individual
    best = path
    numberOfIteration = int(0.30 * len(path))
    while numberOfIteration > 0:
        i = random.randint(0, len(path) - 2)  # len(path)-1)
        j = random.randint(i + 1, (len(individual) - 1))  # len(path)
        if j - i == 1: continue
        new_route = path[:]
        new_route[i:j] = reversed(new_route[i:j])
        if graph.cost(new_route) < graph.cost(best):
            best = new_route
        path = best
        numberOfIteration -= 1
    return path


def repairWith2OPT(graph, individual):
    new_individual = two_opt(graph, individual)
    return new_individual


def mutatePopulation(graph, population, mutationRate):
    mutatedPopulation = []

    for i in range(0, len(population)):
        # mutated = mutateByTwoSwaps(population[i], mutationRate)
        mutated = mutateByInvert(population[i], mutationRate)
        mutatedPopulation.append(mutated)

    # two individuals will be improving by 2opt
    # można wyłączyć opcję i sprawdzić różnicę
    mutatedPopulation[0] = repairWith2OPT(graph, mutatedPopulation[0])
    mutatedPopulation[1] = repairWith2OPT(graph, mutatedPopulation[1])
    # print("mutatedPopulation ", mutatedPopulation)
    return mutatedPopulation


# step 5
# stop condition
def newGeneration(G, generation, eliteSize, mutationRate):
    # print("fitnessList")
    fitnessList = allFitness(G, generation)
    # print(fitnessList)
    routeRank = sortRoutesByFitness(fitnessList)
    # print("sorted list")
    # print(" routeRank size ", len(routeRank))
    #selection = roulette(routeRank, eliteSize)
    k = int(len(routeRank) / 4) #zastanowić się nad doborem parametru
    selection = tournamentSelection(routeRank, eliteSize, k)
    # print("selectionSize ", len(selection))
    parents = getParents(generation, selection)
    # print("parents population size ", len(parents))
    # print(parents)
    # print("children")
    childrensPopulation = generateChildrenPopulation(G, parents, eliteSize)
    # print("childrens population size ", len(childrensPopulation))
    # print("children ", childrensPopulation)
    # print("mutation")
    mutatedPopulation = mutatePopulation(G, childrensPopulation, mutationRate)

    return mutatedPopulation, routeRank


def geneticTSP(G, populationSize, eliteSize, mutationRate, numberOfIterations):
    initialPopulation = createInitialPopulation(G, populationSize)
    fitnessOfInitialPopulation = allFitness(G, initialPopulation)
    initialPopulationRank = sortRoutesByFitness(fitnessOfInitialPopulation)
    initialDistance = 1 / initialPopulationRank[0][1]
    print("Initial distance: ", initialDistance)
    population = initialPopulation
    distanceList = []

    for i in range(0, numberOfIterations):
        population, populationRank = newGeneration(G, population, eliteSize, mutationRate)
        # print("iteracja ", i)
        # print("rozmiar pierwszego z populacji: ", len(population[0]))
        # fitness = allFitness(G, population)
        # populationRank = sortRoutesByFitness(fitness)
        currentDistance = 1 / populationRank[0][1]
        distanceList.append(currentDistance)
        # print("population size ", len(population))
        print(currentDistance)
        if len(population) == 1:
            print("execute only number of iterations: ", i)
            break

    # fitness = allFitness(G, population)
    # populationRank = sortRoutesByFitness(fitness)
    # finalDistance = 1 / populationRank[0][1]
    # print("Final distance: ", finalDistance)
    bestPath = population[populationRank[0][0]]
    plt.figure()
    plt.plot(distanceList)
    plt.xlabel("population: " + str(populationSize) + "elite: " + str(eliteSize) + "mutation: " + str(
        mutationRate) + "iter: " + str(numberOfIterations))
    plt.savefig('plots/' + "p" + str(populationSize) + "e" + str(eliteSize) + "m" + str(mutationRate) + "i" + str(
        numberOfIterations) + '.png')
    print(bestPath)
    print(len(bestPath))
    return bestPath
