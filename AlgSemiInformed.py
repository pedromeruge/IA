from asyncio import Queue
import asyncio
import heapq
from Graph import Graph 
from Node import Node
from Package import Package
from queue import Queue
from BaseAlgorithms import BaseAlgorithms

class AlgSemiInformed:
    def __init__(self):
        print("Calculating semiInformed")

    # devolve map que associa a cada nodo heurística baseada em limite de tempo mais proximo
    # Args:
    # 
    def calculate_heuristic_urgency(self, graph, packages):
        node_visit_order = []
        sorted_packages = sorted(packages, key=Package.getEndTime) # sort packages by delivery urgency
        for package in sorted_packages:
            n1 = graph.get_node_by_name(package.getLocation())
            node_visit_order.append(n1)
        return node_visit_order
    
    # Args:
    #recebe grafo, 
    # nome do nodo inicial, 
    # lista de pacotes a entregar,
    # funcão de calculo de (custo,path) entre dois nodos -!!- tem de receber como args: grafo, nome inicio, nome final, [], set()

    def CalcFunc_with_timeframes(self, graph, start, packages, path_func):

        # lista com nodos por visitar, ordenado por proximidade de data limite
        node_visit_order = self.calculate_heuristic_urgency(graph,packages)

        # print da ordem atribuída a nodos
        # for node in node_visit_order:
        #     print(node)

        errorFlag = False
        finalPath = [start]
        totalCost = 0
        next = Node(start)

        while len(node_visit_order) > 0 and not errorFlag:
            # print("Array before iteration decision: ")
            # for node in node_visit_order:
            #     print(node)
            prev = next
            next = node_visit_order.pop(0)
            # print("This iteration start: " + prev.getName() + ", end: " + next.getName())
            # print("Searching for path between " + prev.getName() + " and " + next.getName())
            result = path_func(graph,prev.getName(),next.getName())
            if result is not None :
                (path,cost) = result # resultado de DFS
                # print("result of " + path_func.__name__ + " iteration: "); print (path); print(cost)
                path.pop(0) # removemos a primeira posição do path obtido, porque já consta na lista final
                finalPath.extend(path)
                totalCost += cost
                # node_visit_order.pop(0) # remover primeiro nodo da lista, continuar a procura
            else :
                errorFlag = True

        if (len(node_visit_order) == 0) and not errorFlag: # necessário o not errorFlag??
            return (finalPath,totalCost)
        
        print('Path does not exist!')
        return None
    
