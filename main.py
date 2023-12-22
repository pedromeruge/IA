from Graph import Graph
from Node import Node
from Package import Package
from Algorithms import Algorithms
from BaseAlgorithms import BaseAlgorithms

def main():
    elvas = Node("elvas")
    estremoz = Node("estremoz")
    evora = Node("evora")
    borba = Node("borba")
    anturas = Node("anturas")

    p1 = Package("estremoz","2023-12-07 09:00","2023-12-07 09:30")
    p2 = Package("evora","2023-12-07 09:00","2023-12-07 09:30")
    p3 = Package("borba","2023-12-07 09:00","2023-12-07 09:45")
    p4 = Package("anturas","2023-12-07 09:00","2023-12-07 09:35")

    g = Graph()

    g.add_edge(elvas,estremoz,2)
    g.add_edge(elvas, borba, 3)
    g.add_edge(elvas,evora,1)
    g.add_edge(estremoz, anturas, 4)
    g.add_edge(evora, anturas, 5)
    g.add_edge(estremoz,borba,2)
    g.add_edge(evora,borba,2)

    a = Algorithms()
    b = BaseAlgorithms()
    packages_locations = [p1,p2,p3,p4]

    #delivery_locations = {"elvas","estremoz","evora","borba","anturas"}

    #(path, custo) = a.greedy_tsp_with_timeframes(g,"elvas",delivery_locations)

    #print (path)
    
    goals = set(package.getLocation() for package in packages_locations)
    
    # resultDFS = a.procura_DFS(g,"elvas",goals)
    # print (f'DFS: {resultDFS}')
    
    # resultBFS = a.procura_BFS(g,"elvas",goals)
    # print (f'BFS: {resultBFS}')
    
    # resultUniforme = a.procura_Uniforme(g,"elvas",goals)
    # print (f'Uniforme: {resultUniforme}')

    path_func = b.procura_BFS # função que calcula caminho entre dois nodos
    result = a.CalcFunc_with_timeframes(g,"elvas",packages_locations,path_func)
    if result is not None:
        (path,custo) = result
        print (path)
        print (custo)
    else:
        print("Error calculating" + path_func.__name__)
        
if __name__ == "__main__":
    main()