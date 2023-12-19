from Graph import Graph 
from Node import Node

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
    
