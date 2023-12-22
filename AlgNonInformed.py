from asyncio import Queue
import asyncio
import heapq
from Graph import Graph 
from Node import Node
from Package import Package
from queue import Queue

class AlgNonInformed:
    def __init__(self):
        print("Calculating non informed")

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
