import sys
from graph import GenerateGraph
import geneticTSP

# if(sys.argv[1]=="generate"):
#     if len(sys.argv)==6:
#         i=GenerateGraph(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))
#     elif len(sys.argv)==5:
#         i=GenerateGraph(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
# if(sys.argv[1]=="load"):
#     i = Graph(sys.argv[2])
# if(sys.argv[1]=="test" and sys.argv[2]=="prd"):
#     i = TestPrd()
# if(sys.argv[1]=="test" and sys.argv[2]=="time"):
#     i = TestTime()
# elif(sys.argv[1]=="analyze" and sys.argv[2]=="random"):
#     i = RandomAnalysis(sys.argv[3])
# else:
#     print("Unsupported type")
#     print("main.py <load> <filename>")
#     print("OR")
#     print("main.py <generate> <type> <dimension> <seed> <upper_bound (optional, default=100)>")
#     print("OR")
#     print("main.py analyze random <filename>")

def main():
     G = GenerateGraph('FULL_MATRIX', 10, 50)
     print("generated graph: ")
     print(G.matrix)

     #odkomentuj to zamiast linijki geneticTSP.geneticTSP(G, 5, 0, 0.05, 10)
     # print("initial population")
     # initialPopulation = geneticTSP.createInitialPopulation(G, 5)
     # print("fitness")
     # fitnessList = geneticTSP.allFitness(G, initialPopulation)
     # print("sorted list")
     # routeRank = geneticTSP.sortRoutesByFitness(fitnessList)
     # print("selection")
     # selection = geneticTSP.roulette(routeRank, 2)
     # print("parents")
     # parents = geneticTSP.getParents(initialPopulation, selection)
     # print("children")
     # childrensPopulation = geneticTSP.generateChildrenPopulation(parents, 1)
     # print("mutation")
     # mutatedPopulation = geneticTSP.mutatePopulation(childrensPopulation, 0.05)

     geneticTSP.geneticTSP(G, 5, 0, 0.05, 10)


main()