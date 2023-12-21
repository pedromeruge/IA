from asyncio import Queue
import asyncio
import heapq
from Graph import Graph 
from Node import Node
from queue import Queue

class Algorithms:
    def __init__(self):
        print("Calculating heuristics")
    # devolve map que associa a cada nodo heurística baseada em limite de tempo mais proximo
    # Args:
    # 
    def calculate_heuristic_urgency(self, graph, delivery_locations):
        node_heuristics = {}
        for location in delivery_locations:
            n1 = graph.get_node_by_name(location)
            node_heuristics[location] = n1.getEndTime() # heuristica de cada nodo é a data de entrega de uma determinada encomenda
        return node_heuristics
    

    # Args:
    #recebe grafo, 
    # nome do nodo inicial, 
    # set de nomes de locais de entrega, 
    # tempo atual
    def greedy_tsp_with_timeframes(self, graph, start, node_locations, currTime=0):
        # open_list é uma lista de nodos visitados, mas com vizinhos
        # closed_list é uma lista de nodos visitados
        # e todos os seus vizinhos também já o foram
        open_list = set([start])
        closed_list = set([])

        # copia do set de locais a visitar, porque este vai ser modificado
        delivery_locations = node_locations.copy()

        # dicionario para armazenar heuristicas que orientam procura greedy
        node_heuristics = self.calculate_heuristic_urgency(graph,node_locations)
        # parents é um dicionário que mantém o antecessor de um nodo
        # começa com start

        parents = {}
        parents[start] = start

        while len(delivery_locations) > 0:

            print(delivery_locations)
            n = None
            prev = n 
            # encontra nodo com a menor heuristica
            for v in open_list:
                # se prazo de término de um for menor que outro
                if n == None or node_heuristics[v] < node_heuristics[n]:
                    n = v
                # se prazo igual, desempatar com menor distância
                elif node_heuristics[v] == node_heuristics[n]:
                    n = v if graph.get_arc_cost(v,prev) < graph.get_arc_cost(n,prev) else n

            if n == None:
                print('Cannot deliver all packages!')
                return None

            print("picked",n)
            # se o nodo corrente é o último a entregar
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor
            if len(delivery_locations) == 1:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, graph.calcula_custo(reconst_path))
            
            # para todos os vizinhos  do nodo corrente
            for (m, weight) in graph.getNeighbours(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            if n in delivery_locations:
                delivery_locations.remove(n)
            closed_list.add(n)

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
