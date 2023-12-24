from Graph import Graph
from Node import Node
from Package import Package

# TOCONSIDER: se passar por nodo onde há encomenda, não entrega logo
#               Posso meter a fazer isso, mas quando acrescentarmos delay de entregar (entrega em si demora tempo / cliente pode só querer entrega a partir de x horas depois) pode impedir que se faça entrega no destino final para que se estava a ir
#               Por isso não meti para já pelo menos
class AlgInformed:

    # retorna set ordenado com ordem de visita de packages, baseada no tempo limite de entrega mais próximo
    def calculate_heuristic_urgency(self, graph, packages):
        node_visit_order = []
        sorted_packages = sorted(packages.values(), key=Package.getEndTime) # sort packages by delivery urgency
        for package in sorted_packages:
            n1 = graph.get_node_by_name(package.getLocation())
            node_visit_order.append(n1)
        return node_visit_order
    
    def add_positions_to_nodes(self,graph,node_positions):
        for location, coords in node_positions.items():
            graph.add_heuristica(location, coords)
            # print("Location: " + location + " (" + str(coords[0]) + "," + str(coords[1]) + ")")
        
    #calcular heurística de nodo baseada na dist de nodo atual com nodo pretendido
    def calculate_node_heuristic(self, graph, curr, end):
        (currX,currY) = graph.get_heuristica(curr)
        (endX,endY) = graph.get_heuristica(end)
        res = ((endX-currX)**2 + (endY-currY)**2)
        return res
    
     # Args:
     #recebe grafo, 
     # nome do nodo inicial, 
     # set de nomes de locais de entrega, 
    def procura_informada(self, graph, startPlace, startTime, packages, node_positions, stats, path_func):
        
        # lista com nodos por visitar, ordenado por proximidade de data limite
        node_visit_order = self.calculate_heuristic_urgency(graph,packages)
        # for node in node_visit_order:
        #     print (node)

        # atualiza grafo com as posições para cada nodo
        self.add_positions_to_nodes(graph,node_positions)

        errorFlag = False
        finalPath = [startPlace]
        totalCost = 0
        next = Node(startPlace)

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
    
    def procura_greedy(self, graph, start, end):
        # open_list é uma lista de nodos visitados, mas com vizinhos
        # closed_list é uma lista de nodos visitados
        # e todos os seus vizinhos também já o foram
        open_list = set([start])
        closed_list = set([])

        # parents é um dicionário que mantém o antecessor de um nodo
        # começa com start
        parents = {}
        parents[start] = start

        while len(open_list) > 0:

            n = None
            # encontra nodo com a menor heuristica
            for v in open_list:

                # distancia em relação ao próximo nodo a visitar
                if n == None or self.calculate_node_heuristic(graph,v,end) < self.calculate_node_heuristic(graph,n,end):
                    n = v

            if n == None:
                print('Cannot deliver package!')
                return None

            # print("picked",n)
            # se o nodo corrente é o último a entregar
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, graph.calcula_custo(reconst_path))

            # para todos os vizinhos  do nodo corrente
            for (m, peso) in graph.getNeighbours(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None
    
    def procura_aStar(self, graph, start, end):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = {start}
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}  ##  g é apra substiruir pelo peso  ???

        g[start] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start
        #n = None
        while len(open_list) > 0:
            # find a node with the lowest value of f() - evaluation function
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                ##if n == None or g[v] + self.getH(v) < g[n] + self.getH(n):  # heuristica ver.....
                if n == None or g[v] + self.calculate_node_heuristic(graph,v,end) < g[n] + self.calculate_node_heuristic(graph,n,end):  # heuristica ver.....
                    n = v
            if n == None:
                print('Cannot deliver package!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, graph.calcula_custo(reconst_path))

            # for all neighbors of the current node do
            for (m, weight) in graph.getNeighbours(n):  # definir função getneighbours  tem de ter um par nodo peso
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None