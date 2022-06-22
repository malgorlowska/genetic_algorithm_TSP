from read import Graph
from graph import GenerateGraph
import numpy as np
from operator import itemgetter
from geneticTspForIslands import geneticTSP

file = "bays29.tsp"

G = Graph(file)

populationSizee = 20

def createInitialPopulation(graph, populationSize):
    population = []
    for i in range(0, populationSize):
        population.append(GenerateGraph.random_method(graph))
    return population


def createIslands(numOfIsland, population):
    islands = []
    count = int(len(population)/numOfIsland)
    for i in range(0, populationSizee,count):
        islands.append(population[i:i+count])
    return islands

def averageFitness(graph, population):
    fitness = np.zeros(len(population))
    for i in range(0, len(population)):
        fitness[i] = graph.cost(population[i])  # upewnić się czy cost dodaje też koszt od ostatniego do pierwszego!

    # print("fitness ", fitness)
    return sum(fitness)/len(fitness)

def sortIslandsByHierarchy(graph, islands):

    hierarchy = []
    myorder = []

    for i in range(len(islands)):
        average = averageFitness(graph, islands[i])
        x = [i, average]
        hierarchy.append(x)

    hierarchy = sorted(hierarchy, key=itemgetter(1))

    for j in range(len(islands)):
        myorder.append(hierarchy[j][0])

    islands = [islands[k] for k in myorder]
    return islands, hierarchy

def bestCandidate(population):
    bestCost = 10000000
    candidate = 0
    for i in range(len(population)):
        cost1 = G.cost(population[i])
        if(cost1<bestCost):
            bestCost = cost1
            candidate = i
    return population[candidate]

def migrationSelection(islands, graph):
    islands1, hierarchy = sortIslandsByHierarchy(graph, islands)

    migrationCandidates = []

    for j in range(len(islands1)):

        island = islands1[j]

        averageFitness1 = hierarchy[j]
        x = []
        for i in range(len(island)):
            cost = graph.cost(island[i])
            if(cost>=averageFitness1[1]):
                x.append(i)
        migrationCandidates.append(x)

    return migrationCandidates


def eliteSelection(islandWithMigrants, islands):

    candidateAncCost = []
    order = []

    print("Island with Migrants First" + str(islandWithMigrants))

    for i in range(len(islandWithMigrants)):
        cost = G.cost(islandWithMigrants[i])
        candidateAncCost.append([i,cost])

    candidateAncCost = sorted(candidateAncCost, key = itemgetter(1))
    print("hierarchyelite" + str(candidateAncCost))

    for j in range(len(candidateAncCost)):
        order.append(candidateAncCost[j][0])
    print("order" + str(order))
    islandWithMigrants = [islandWithMigrants[k] for k in order]
    print("islandwithMigrants" + str(islandWithMigrants))
    newIsland = islandWithMigrants[:5]
    print("New Island" + str(newIsland))

    return newIsland


def migration(islands, migrationCandidates, graph):

    for i in range(len(islands)-1):
        currentIsland = islands[i]
        migrationIsland = islands[i+1]

        for j in range(len(migrationCandidates[i+1])):
            print(migrationCandidates)
            print(migrationCandidates[i])
            migrate = migrationIsland[migrationCandidates[i+1][j]]
            currentIsland.append(migrate)

        currentIsland = eliteSelection(currentIsland, islands)
        islands[i] = currentIsland

    lastIsland = islands[-1]
    goodLength = len(islands[0])
    print(migrationCandidates[-1])
    print(len(migrationCandidates[-1]))

    for k in range(len(migrationCandidates[-1])):
        lastIsland.pop(migrationCandidates[-1][0])

    for i in range(goodLength-len(lastIsland)):
        lastIsland.append(GenerateGraph.random_method(graph))

    islands[-1] = lastIsland

    return islands


def GeneticIslands(numOfIslands, numOfepocs):

    initialPopulation = createInitialPopulation(G, populationSizee)
    islands = createIslands(numOfIslands, initialPopulation)

    for i in range(numOfepocs):
        print("Epoka: " + str(i))
        for j in range(len(islands)):
            print(islands[j])
            islands[j] = geneticTSP(G, 4, 0.03, 29, 0,1,1,islands[j])

        islands, hierarchy = sortIslandsByHierarchy(G, islands)
        migrationCandidates = migrationSelection(islands, G)
        islands = migration(islands, migrationCandidates, G)

    finalIslands, hierarchy = sortIslandsByHierarchy(G, islands)

    finalIsland = finalIslands[0]

    bestPath= bestCandidate(finalIsland)
    print(bestPath)
    bestCost = G.cost(bestPath)

    print("Najlepsza Sciezka: " + str(bestPath) + "Koszt: " + str(bestCost))
    prd = Graph.PRD(G, bestCost)
    prd = abs(prd)
    print("Prd: " + str(prd))

if __name__ == "__main__":

    GeneticIslands(4, 4)