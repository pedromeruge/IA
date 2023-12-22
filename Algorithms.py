from asyncio import Queue
import asyncio
import heapq
from Graph import Graph 
from Node import Node
from Package import Package
from queue import Queue
from BaseAlgorithms import BaseAlgorithms

class Algorithms:
    def __init__(self):
        print("Calculating heuristics")

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
    

    def procura_DFS(self, graph, start, goals, path=[], visited=set()):
        path.append(start)          # Adiciona o node atual ao caminho
        visited.add(start)          # Marca o node atual como visitado

        remaining_goals = set(goals)  # Cria uma cópia dos goals restantes

        if not remaining_goals:
            custo_total = graph.calcula_custo(path)
            return (path, custo_total)  # Retorna o caminho e o custo total se todos os goals foram encontrados

        for adjacent_node in graph.getNeighbours(start):
            adjacent_node = adjacent_node[0]
            if adjacent_node not in visited:
                if adjacent_node in remaining_goals:
                    remaining_goals.remove(adjacent_node)
                    result = self.procura_DFS(
                        graph, adjacent_node, remaining_goals, path, visited
                    )
                    if result is not None:
                        return result
                else:
                    result = self.procura_DFS(
                        graph, adjacent_node, remaining_goals, path, visited
                    )
                    if result is not None:
                        return result

        path.pop()  # Desfaz a escolha do node atual se não levar a uma solução
        return None 

    def procura_BFS(self, graph, start, goals):
        visited = set()       
        queue = Queue()              
        parent = {} # Dicionário para armazenar o pai de cada nó

        queue.put(start)
        visited.add(start)
        parent[start] = None

        remaining_goals = set(goals)  # Cria uma cópia dos nodes objetivo restantes

        expansion_path = []

        while not queue.empty():
            current_node = queue.get()
            expansion_path.append(current_node)

            for neighbour in graph.getNeighbours(current_node):
                neighbour = neighbour[0]
                if neighbour not in visited:
                    queue.put(neighbour)
                    visited.add(neighbour)
                    parent[neighbour] = current_node

            if current_node in remaining_goals:
                remaining_goals.remove(current_node)

            if not remaining_goals:
                # Todos os goals visitados
                cost = graph.calcula_custo(expansion_path)
                return expansion_path, cost

        # Se nenhum caminho for encontrado
        return None, 0


    def procura_Uniforme(self, graph, start, goals):
        priority_queue = [(0, start, [])]
        visited = set()
        expansion_order = []  # armazenar a ordem de expansão

        remaining_goals = set(goals)
        total_cost = 0 

        while priority_queue and remaining_goals:
            (current_cost, current_node, path) = heapq.heappop(priority_queue)

            if current_node in visited:
                continue

            path = path + [current_node]
            expansion_order.append(current_node)

            visited.add(current_node)

            if current_node in remaining_goals:
                remaining_goals.remove(current_node)

                # goal alcançado
                if not remaining_goals:
                    total_cost = current_cost

            for (neighbour, neighbour_cost) in graph.getNeighbours(current_node):
                if neighbour not in visited and neighbour not in path:
                    # atualizar o custo
                    new_cost = current_cost + neighbour_cost
                    heapq.heappush(priority_queue, (new_cost, neighbour, path + [neighbour]))

        # Se nenhum caminho for encontrado
        return expansion_order, total_cost
