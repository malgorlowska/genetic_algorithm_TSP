from matplotlib import pyplot as plt
import sys
import random
import copy
import time
import os
import psutil
import geneticTSP

class Graph:
    supported_formats = ['FULL_MATRIX', 'EUC_2D', 'LOWER_DIAG_ROW']
    supported_format_keys = ['EDGE_WEIGHT_FORMAT', 'EDGE_WEIGHT_TYPE']

    supported_header_delimiters = ['NODE_COORD_SECTION', 'EDGE_WEIGHT_SECTION']

    edge_weight_format = ""

    header = dict()
    optimal={"br17.atsp": 39, "gr24.tsp": 1278,"bays29.tsp": 2108,"berlin52.tsp": 7542,"eil76.tsp": 570,"eil101.tsp": 2918, "lin105.tsp": 14941, "gr120.tsp": 6942, "ftv44.atsp": 1613, "ftv70.atsp": 1950, "kro124p.atsp": 36230}
    matrix = []
    coordinates = dict()
    path = []

    def __init__(self, filename):
        self.filename = filename
        self.read_data_from = {
            "FULL_MATRIX": self.read_data_from_full_matrix,
            "EUC_2D": self.read_data_from_euc_2d,
            "LOWER_DIAG_ROW": self.read_data_from_lower_diag_row
        }
        self.read()
        #self.show_matrix()
        #self.show_solution()
        #print("długosc testowa")

    def read(self):
        with open(self.filename, 'r') as file:
            for line in file:
                line = line.replace(":", "")
                if any(x in line for x in self.supported_header_delimiters):
                    break
                split = [x.strip() for x in line.split(maxsplit=1)]
                if len(split) < 2:
                    break
                key, value = split
                self.header[key] = value

            self.set_edge_weight_format()
            self.set_dimension()

            if self.edge_weight_format not in self.supported_formats:
                print("Unsupported data format")
                exit(1)

            self.matrix = [[0 for y in range(0, self.dimension)] for x in range(0, self.dimension)]
            self.read_data_from[self.edge_weight_format](file)

            bagno = self.matrix
        return bagno


    def set_edge_weight_format(self):
        for format_key in self.supported_format_keys:
            if format_key in self.header.keys():
                self.edge_weight_format = self.header[format_key]
                break

    def set_dimension(self):
        self.dimension = int(self.header["DIMENSION"])
        self.path = [x for x in range(0, self.dimension)]

    def read_data_from_full_matrix(self, file):
        numbers = self.read_numbers(file)
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                self.matrix[i][j] = int(numbers[i * self.dimension + j])

    def read_data_from_lower_diag_row(self, file):
        numbers = self.read_numbers(file)
        index = 0
        for i in range(0, self.dimension):
            for j in range(0, i + 1):
                self.matrix[i][j] = self.matrix[j][i] = numbers[index]
                index += 1

    def read_data_from_euc_2d(self, file):
        numbers = [a for a in [x.split() for x in file.readlines()] if len(a) == 3]
        index = 0
        for i in range(0, self.dimension):
            ni, ni_x, ni_y = numbers[i]
            self.coordinates[int(ni)] = {'x': int(float(ni_x)), 'y': int(float(ni_y))}
            for j in range(0, i + 1):
                nj, nj_x, nj_y = numbers[j]
                distance = int(((float(ni_x) - float(nj_x)) ** 2 + (float(ni_y) - float(nj_y)) ** 2) ** 0.5)
                self.matrix[i][j] = self.matrix[j][i] = distance
                index += 1

    def show_matrix(self):
        for subset in self.matrix:
            print(subset)
        self.draw()


    def draw(self):
        if self.edge_weight_format == 'EUC_2D':
            # draw lines
            for i in range(0, self.dimension):
                ni = self.coordinates[i + 1]
                for j in range(0, i):
                    nj = self.coordinates[j + 1]
                    plt.plot([ni['x'], nj['x']], [ni['y'], nj['y']], color="red", linewidth=0.1)
            # draw points
            for node in self.coordinates.values():
                plt.plot(node['x'], node['y'], color="blue", marker="o", markersize=2)
            plt.show()


    def test_cost(self,vertex):
        distance=0
        for i in range(len(vertex)):
            if i+1==len(vertex):
                print(self.matrix[vertex[i]][vertex[0]])
                distance=distance+int(self.matrix[vertex[i]][vertex[0]])
                break
            print(self.matrix[vertex[i]][vertex[i+1]])
            distance=distance+int(self.matrix[vertex[i]][vertex[i+1]])


    '''
    def k_random_method(self):
        found_zero=False
        k=1000
        print("k: ",k)
        min_dist=sys.maxsize
        vertex=[x for x in range(self.dimension)]
        path=[]
        for j in range(k):
            random.shuffle(vertex)
            distance=0
            for i in range(len(vertex)):
                if i+1==len(vertex):
                    distance=distance+int(self.matrix[vertex[i]][vertex[0]])
                    break
                if(self.matrix[vertex[i]][vertex[i+1]]==0):
                    found_zero=True
                    break
                distance=distance+int(self.matrix[vertex[i]][vertex[i+1]])
            if(found_zero):
                found_zero=False
                continue
            if(distance<min_dist):
                min_dist=distance
                path=vertex.copy()
        print("Droga: ",min_dist)
        self.test_cost(path)
        print("Cykl: ",path)
        if self.edge_weight_format == 'EUC_2D':
            self.draw_solution(path)
        self.PRD(min_dist)
        '''

    def k_random_method(self):
        start_time = time.time()
        k=100
        print("k: ",k)
        min_dist=sys.maxsize
        vertex=[x for x in range(self.dimension)]
        path=[]
        for j in range(k):
            random.shuffle(vertex)
            distance=0
            for i in range(len(vertex)):
                if i+1==len(vertex):
                    distance=distance+int(self.matrix[vertex[i]][vertex[0]])
                    break
                if(int(self.matrix[vertex[i]][vertex[i+1]])==0):
                    continue
                distance=distance+int(self.matrix[vertex[i]][vertex[i+1]])
            if(distance<min_dist):
                min_dist=distance
                path=vertex.copy()
        print("Droga: ",min_dist)
        print("Cykl: ",path)
        #self.test_cost(path)
        if self.edge_weight_format == 'EUC_2D':
            self.draw_solution(path)
        self.PRD(min_dist)
        print("Czas: %s " % (time.time()-start_time))
        process = psutil.Process(os.getpid())
        print("Pamięć: %s" % process.memory_info().rss)

    def nearest_neighbor(self):
        start_time = time.time()
        start=random.randint(0,self.dimension-1)
        #print(start)
        path=[start]
        min_dist=0
        matrix_copy=copy.deepcopy(self.matrix)
        while(len(path)!=self.dimension):
            distances=matrix_copy[start]
            distances.sort()
            counter=0
            j=0
            while j < self.dimension:
                if distances[counter]==self.matrix[start][j]:
                    if j not in path:
                        if(distances[counter]==0):
                            counter=counter+1
                            j=-1
                        else:
                            min_dist=min_dist+int(distances[counter])
                            path.append(j)
                            start=j
                            counter=0
                            break
                j=j+1
                if(j==self.dimension):
                    j=0
                    counter=counter+1
                if(counter==self.dimension):
                    print("Ślepy zaułek")
                    return
        print("Droga: ",min_dist)
        #self.test_cost(path)
        print("Cykl: ",path)
        if self.edge_weight_format == 'EUC_2D':
            self.draw_solution(path)
        self.PRD(min_dist)
        print("Czas: %s " % (time.time()-start_time))
        process = psutil.Process(os.getpid())
        print("Pamięć: %s" % process.memory_info().rss)

    def extended_nearest_neighbor(self):
        currentStart = 0
        start_time = time.time()
        for i in range(0,self.dimension):
            start= i
            #print(start)
            path=[start]
            min_dist=0
            matrix_copy=copy.deepcopy(self.matrix)
            while(len(path)!=self.dimension):
                distances=matrix_copy[start]
                distances.sort()
                counter=0
                j=0
                while j < self.dimension:
                    if distances[counter]==self.matrix[start][j]:
                        if j not in path:
                            if(distances[counter]==0):
                                counter=counter+1
                                j=-1
                            else:
                                min_dist=min_dist+int(distances[counter])
                                path.append(j)
                                start=j
                                counter=0
                                break
                    j=j+1
                    if(j==self.dimension):
                        j=0
                        counter=counter+1
                    if(counter==self.dimension):
                        print("Ślepy zaułek")
                        return
        print("Droga: ",min_dist)
        #self.test_cost(path)
        print("Cykl: ",path)
        if self.edge_weight_format == 'EUC_2D':
            self.draw_solution(path)
        self.PRD(min_dist)
        print("Czas: %s " % (time.time()-start_time))
        process = psutil.Process(os.getpid())
        print("Pamięć: %s" % process.memory_info().rss)


    def cost(self,vertex):
        distance=0
        for i in range(len(vertex)):
            if i+1==len(vertex):
                distance=distance+int(self.matrix[vertex[i]][vertex[0]])
                break
            distance=distance+int(self.matrix[vertex[i]][vertex[i+1]])
        return distance

    def two_opt(self):
        start_time = time.time()
        path = [x for x in range(self.dimension)]
        best = path
        improved = True
        while improved:
            improved = False
            for i in range(0, len(path)-1):
                for j in range(i+1, len(path)):
                    if j-i == 1: continue
                    new_route = path[:]
                    new_route[i:j] = reversed(new_route[i:j])
                    if self.cost(new_route) < self.cost(best):
                        best = new_route
                        improved = True
            path = best
        print("Droga: ",self.cost(best))
        print("Cykl: ", path)
        #self.test_cost(path)
        if self.edge_weight_format == 'EUC_2D':
            self.draw_solution(best)
        self.PRD(self.cost(best))
        print("Czas: %s " % (time.time()-start_time))
        process = psutil.Process(os.getpid())
        print("Pamięć: %s" % process.memory_info().rss)

    def show_solution(self):
        print("Metoda k-random: ")
        self.k_random_method()
        print("Metoda najbliższego sąsiada: ")
        self.nearest_neighbor()
        print("Roszerzona metoda najbliższego sąsiada: ")
        self.extended_nearest_neighbor()
        print("Algorytm 2-OPT: ")
        self.two_opt()
        print("genetic: ")
        geneticTSP.geneticTSP(self.matrix, 10, 2, 0.02, 40)




    def draw_solution(self,path):
        for i in range(0, len(path)-1):
            ni=self.coordinates[path[i]+1]
            nj=self.coordinates[path[i+1]+1]
            plt.plot([ni['x'], nj['x']], [ni['y'], nj['y']], color="red", linewidth=0.1)
        for node in self.coordinates.values():
            plt.plot(node['x'], node['y'], color="blue", marker="o", markersize=2)
        plt.show()

    def PRD(self,x):
        ref=self.optimal[self.filename]
        result=100*(x-ref)/ref
        #print("PRD(x):{}%".format(result))
        return result

    @staticmethod
    def read_numbers(file):
        return [item for sublist in [x.split() for x in file.readlines()] for item in sublist if
                item.isnumeric()]