
import sys
from graph import GenerateGraph
import geneticTSP
import readFile
import read

# if(sys.argv[1]=="generate"):
#     if len(sys.argv)==6:
#         i=GenerateGraph(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))
#     elif len(sys.argv)==5:
#         i=GenerateGraph(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
#if(sys.argv[1]=="load"):
#i = Graph(sys.argv[2])
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



    try:
        files = ["bays29.tsp", "berlin52.tsp", "eil76.tsp", "eil101.tsp", "lin105.tsp", "gr120.tsp"]
        populationList = [52]
        eliteList = [17]
        mutationRateList = [0.03]
        iterations = [150]
        muteTab = [0,1]
        crossTab = [0,1]
        selectTab = [0,1]


        baysBest=berlinBest= eilBest= eil2Best= linBest= gr2Best = 1000000000
        baysPrd=berlinPrd= eilPrd= eil2Prd= linPrd= gr2Prd = 101
        arr0 = arr1 = arr2 = arr3 = arr4 = arr5 = [0,0,0,0,0,0,0]


        file1 = files[1]
        for i in range(len(populationList)):
            population = populationList[i]
            for j in range(len(eliteList)):
                elite = eliteList[j]
                for k in range(len(mutationRateList)):
                    mutation = mutationRateList[k]
                    for l in range(len(iterations)):
                        it = iterations[l]
                        for m in range(len(muteTab)):
                            mutationType = muteTab[m]
                            for n in range(len(crossTab)):
                                crossType = crossTab[n]
                                for o in range(len(selectTab)):
                                    selectType = selectTab[o]



                                    G = read.Graph(file1)
                                    bestPath, prd, cost = geneticTSP.geneticTSP(G, population, elite, mutation,it, selectType, mutationType, crossType)


                                    berlinBest = cost

                                    berlinPrd = prd
                                    arr1 = [populationList[i],eliteList[j],mutationRateList[k],iterations[l],m,n,o]



                                    print("Best result for: " + str(files[1]) + " Cost: " + str(berlinBest) + " Prd: " + str(berlinPrd) + " Parameters: " + str(arr1))
                                    f = open("ResultsAdaptingBertlin52Part3" + str(m) + str(n) + str(o) + ".txt", "x")
                                    f.write("Best result for: " + str(files[1]) + " Cost: " + str(berlinBest) + " Prd: " + str(berlinPrd) + " Parameters: " + str(arr1))
                                    f.close()

    except:
        pass

main()