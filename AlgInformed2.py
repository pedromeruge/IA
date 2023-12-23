from Graph import Graph
from Node import Node
from Package import Package
from datetime import datetime

# TOCONSIDER: se passar por nodo onde há encomenda, não entrega logo
#               Posso meter a fazer isso, mas quando acrescentarmos delay de entregar (entrega em si demora tempo / cliente pode só querer entrega a partir de x horas depois) pode impedir que se faça entrega no destino final para que se estava a ir
#               Por isso não meti para já pelo menos
class AlgInformed2:
    def __init__(self):
        print("Calculating Informed")

    def add_positions_to_nodes(self,graph,node_positions):
        for (location,x,y) in node_positions:
            graph.add_heuristica(location,(x,y))
            print ("Location: " + location + " (" + str(x) + "," + str(y) + ")")
        
    #calcular heurística de nodo baseada em:
    #   dist (pos atual, pos package mais perto) +
    #   diff(tempo atual, tempo limite) (preciso, porque nodos vizinhos podem estar a distância diferente do nodo atual, resultando em tempos diferentes lá) +
    #   diff(tempo inicial, tempo atual) (se estiver muito longe do início, n vale a pena ir lá)
    #   POR CONSIDERAR: diff(tmepo inicial, tempo final) ??
    def calculate_node_heuristic(self, graph, currNode, packages_left, currTime):
        (currX,currY) = graph.get_heuristica(currNode)
        final_res = float('inf') # guardar a heurística mínima, para todos os packages a ser entregues!!
        temp_res = 0 # em relação a cada package calcular heurística
        for package in packages_left.values():
            place = package.m_location
            startTime = package.m_start_time
            endTime = package.m_end_time
            print(f"package left: {place}, {startTime},{endTime}")
            (endX,endY) = graph.get_heuristica(place)
            temp_res += ((endX-currX)**2 + (endY-currY)**2)
            print (f"Geo diff {temp_res}")
            temp_res += (endTime - currTime).total_seconds() / 60 # time diff in minutes
            print (f"After time {temp_res}")
            # temp_res += (currTime - startTime).total_seconds() / 60 # time diff in minutes
            if (temp_res < final_res):
                final_res = temp_res
        print ("Heuristic obtained: " + str(final_res))
        return final_res
    
    # Args:
    #recebe grafo, 
    # nome do nodo inicial, 
    # set de nomes de locais de entrega, 
    def procura_informada(self, graph, start, packages, node_positions, path_func):

        # atualiza grafo com as posições para cada nodo
        self.add_positions_to_nodes(graph,node_positions)

        to_deliver = {package.m_location: package for package in packages} # map dos pacotes a entregar, location para respetivo pacote (acessos rápidos)
        currTime = datetime.strptime("2023-12-07 08:00", "%Y-%m-%d %H:%M")
        errorFlag = False
        finalPath = [start]
        totalCost = 0
        next = start

        while len(to_deliver) > 0 and not errorFlag:
            prev = next # proximo nodo de que se vai partir
            print("This iteration start: " + prev)

            result = path_func(graph,prev,to_deliver,currTime)
            if result is not None :
                (path,cost) = result
                # print("result of " + path_func.__name__ + " iteration: "); print (path); print(cost)
                path.pop(0) # removemos a primeira posição do path obtido, porque já consta na lista final
                finalPath.extend(path)
                totalCost += cost
                next = path[-1] # próximo nodo em que se começa será o último nodo a que se chegou na iteração anterior

                del to_deliver[next] # remover dos pacotes a entregar o pacote atual

            else :
                errorFlag = True

        if (len(to_deliver) == 0) and not errorFlag: # necessário o not errorFlag??
            return (finalPath,totalCost)
        
        print('Path does not exist!')
        return None
    
    def procura_greedy(self, graph, start, to_deliver, currTime):

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
                if n == None or self.calculate_node_heuristic(graph,v,to_deliver,currTime) < self.calculate_node_heuristic(graph,n,to_deliver,currTime):
                    n = v

            if n == None:
                print('Cannot deliver package!')
                return None

            # se o nodo corrente é o último a entregar
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor
            if n in to_deliver:
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
    
    def procura_aStar(self, graph, start, to_deliver, currTime):
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
                if n == None or g[v] + self.calculate_node_heuristic(graph,v,to_deliver,currTime) < g[n] + self.calculate_node_heuristic(graph,v,to_deliver,currTime):  # heuristica ver.....
                    n = v
            if n == None:
                print('Cannot deliver package!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n in to_deliver:
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