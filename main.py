from Graph import Graph
from Node import Node
from Package import Package
from AlgSemiInformed import AlgSemiInformed
from AlgNonInformed import AlgNonInformed
from AlgInformed import AlgInformed
from BaseAlgorithms import BaseAlgorithms
import random

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

    packages_locations = [p1,p2,p3,p4]

    #### procura nao informada ###############

    # nonInformed = AlgNonInformed()
    # goals = set(package.getLocation() for package in packages_locations)
    
    # resultDFS = nonInformed.procura_DFS(g,"elvas",goals)
    # print (f'DFS: {resultDFS}')
    
    # resultBFS = nonInformed.procura_BFS(g,"elvas",goals)
    # print (f'BFS: {resultBFS}')
    
    # resultUniforme = nonInformed.procura_Uniforme(g,"elvas",goals)
    # print (f'Uniforme: {resultUniforme}')

    ### procura semi informada (mistura de dois algoritmos) ##########

    # semiInformed = AlgSemiInformed()
    # BaseAlgs = BaseAlgorithms()

    # path_func = BaseAlgs.procura_BFS # função que calcula caminho entre dois nodos
    # result = semiInformed.CalcFunc_with_timeframes(g,"elvas",packages_locations,path_func)
    # if result is not None:
    #     (path,custo) = result
    #     print (path)
    #     print (custo)
    # else:
    #     print("Error calculating" + path_func.__name__)
        
    ####### procura informada ###########
    node_positions = []
    node_positions.append(("elvas",5,10))
    node_positions.append(("estremoz",5,8))
    node_positions.append(("anturas",5,2))
    node_positions.append(("evora",4,9))
    node_positions.append(("borba",6,7))
    
    #for node in g.getNodes():   
    #node_positions.append((node.getName(),random.randint(1,20), random.randint(1,20))) # obter lista de posições (x,y) para cada nodo
    # para já fiz assim, mais tarde devia ser atribuir valores razoáveis à mão para cada nodo

    informed = AlgInformed()
    result = informed.procura_greedy(g,"elvas",packages_locations, node_positions)
    if result is not None:
        (path,custo) = result
        print (path)
        print (custo)
    else:
        print("Error calculating greedy")
        
if __name__ == "__main__":
    main()