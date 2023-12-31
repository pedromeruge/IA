import math
from Package import Package
from datetime import timedelta

from Stats import Stats

# TOCONSIDER: se passar por nodo onde há encomenda, não entrega logo
#               Posso meter a fazer isso, mas quando acrescentarmos delay de entregar (entrega em si demora tempo / cliente pode só querer entrega a partir de x horas depois) pode impedir que se faça entrega no destino final para que se estava a ir
#               Por isso não meti para já pelo menos
class AlgInformed:

    # heurística baseada em limite de tempo mais proximo
    # retorna lista ordenado com ordem de visita de packages
    def calculate_heuristic_urgency(self, packages):
        sorted_Nodes = sorted(packages.values(), key=Package.getEndTime) # sort Nodes by delivery urgency
        return sorted_Nodes
    
    # acrescentar valores (x,y) a cada nodo, para utilizar como heurística
    def add_positions_to_nodes(self,graph,node_positions):
        for location, coords in node_positions.items():
            graph.add_heuristica(location, coords)
            # print("Location: " + location + " (" + str(coords[0]) + "," + str(coords[1]) + ")")
        
    #calcular heurística de nodo baseada na dist de nodo atual com nodo pretendido
    def calculate_node_heuristic(self, graph, curr, end):
        (currX,currY) = graph.get_heuristica(curr)
        (endX,endY) = graph.get_heuristica(end)
        res = math.sqrt((endX-currX)**2 + (endY-currY)**2) * 100000
        return res
    
    # decidir qual o melhor transporte de partida, tendo em conta o peso e volume das encomendas
    def get_transport(self, Nodes):
        total_weight = 0
        for Node in Nodes.values():
            total_weight += Node.m_weight
        for transport, weight in Stats.max_peso.items():
            if  total_weight <= weight:
                return (transport, total_weight)
        return None
        # se não houver transporte que dê, retorna que não é possível
    
    # calcular rating para horario em que estafeta entrega pacote
    def calculateRating(self, currTime, location, packages):
        delay = (currTime - packages[location].getEndTime()).total_seconds() / 60 # reduz-se o deliver delay que já foi acrescentado no currTime
        # print (f'Obtained delay: {delay} from endTime: {packages[location].getEndTime().strftime("%Y-%m-%d %H:%M:%S")} and currTime: {currTime.strftime("%Y-%m-%d %H:%M:%S")}')
        for (fixedDelay,rating) in Stats.rating_decr_atraso:
            if delay <= fixedDelay:
                return rating
        return 0 # se entrega for depois de 60 minutos é rating 0

    def procura_informada(self, graph, startPlace, startTime, packages, path_func):
        best_path = []
        best_rating = 0
        best_cost = math.inf
        order_of_visit = []
        best_transport = None
        # obter transporte
        result = self.get_transport(packages)
        if not result: # se não houver veículo que consiga transportar todos os pacotes
            print("No vehicle can hold that many packages due to weight/volume")
            return None
        else:
            (vehicle,total_weight) = result
        
        for transport in Stats.transportes[Stats.transportes.index(vehicle): ]:
            #calcular percurso para cada transporte que aguenta com os pacotes todos
            resultFunc = self.procura_informada_aux(graph, startPlace, startTime, packages, transport, total_weight, path_func)
            if not resultFunc:
                print(f'Path does not exist for {transport}!')
            else:
                (finalPath,totalCost, average_rating, nodesVisited) = resultFunc
                # print(f"For iter {transport} {(finalPath, len(nodesVisited), totalCost, average_rating)}\n")

                if average_rating >= best_rating and totalCost < best_cost:
                    best_path = finalPath
                    best_cost = totalCost
                    best_rating = average_rating
                    best_transport = transport

                order_of_visit += nodesVisited

        if best_cost == math.inf:
            return None
        else:
            return (best_path,best_cost,best_rating,order_of_visit, best_transport)
        
     # Args:
     #recebe grafo, 
     # nome do nodo inicial, 
     # set de nomes de locais de entrega, 
    def procura_informada_aux(self, graph, startPlace, startTime, packages, transport, total_weight, path_func):
        
        # lista com nodos por visitar, ordenado por proximidade de data limite
        package_visit_order = self.calculate_heuristic_urgency(packages)

        currTime = startTime # tempo inicial
        currVelocity = Stats.base_vel[transport] - (total_weight * Stats.vel_decr_peso[transport]) # velocidade inicial
        ratings = [] # lista de ratings acumulados de entregas da pacotes
        errorFlag = False
        finalPath = [startPlace]
        totalCost = 0
        node_visit_order = [] # statistics

        currNode = startPlace

        while len(package_visit_order) > 0 and not errorFlag:
            # print("Array before iteration decision: ")
            # for node in node_visit_order:
            #     print(node)
            prevNode = currNode
            currNode = package_visit_order.pop(0).getLocation() # procurar nodo com encomenda mais urgente da lista

            result = path_func(graph,prevNode,currNode, transport)
            if result is not None :
                (path,distTraveled, visited) = result 
                # print(f'Got from {path_func.__name__} path: {path} dist: {distTraveled}')
                node_visit_order += visited # nodos visitados

                path.pop(0) # removemos a primeira posição do path obtido, porque já consta na lista final
                finalPath.extend(path) # acrescentar caminho desta iteração ao caminho final
                totalCost += distTraveled * Stats.consumo[transport] # somar C02 na deslocação desta iteração ao total
                timeBetweenDeliveries = timedelta(minutes= (distTraveled / currVelocity)) # tempo decorrido nesta iteração
                # print(f"timeBetweenDeliveries: {timeBetweenDeliveries.total_seconds() / 60}")
                currTime = max(packages[currNode].getStartTime(), currTime + timeBetweenDeliveries) # tempo máximo entre: tempo desde entrega anterior até agora ou tempo inicial de entrega para cliente; + tempo fixo de entregar encomenda
                rating = self.calculateRating(currTime,currNode,packages) # obter rating baseado em tempo de atraso da entrega
                currTime = currTime + timedelta(minutes=Stats.deliver_delay) # acrescentar tempo fixo de entrega em qualquer sitio
                ratings.append(rating) # acrescentar rating aos ratings 
                currVelocity += Stats.vel_decr_peso[transport] * packages[currNode].getWeight() # aumentar velocidade com redução de peso da entrega

            else :
                errorFlag = True

        if (len(package_visit_order) == 0) and not errorFlag: # necessário o not errorFlag??
            average_rating = sum(ratings) / len(ratings)

            # print(f'Final CurrTime: {currTime.strftime("%Y-%m-%d %H:%M:%S")}')
            # print(f"Final currVelocity: {currVelocity}")
            # print(f"Final CurrConsumption: {totalCost}")
            # print(f"Final CurrRatings {ratings}")

            return (finalPath,totalCost, average_rating, node_visit_order)

        print('Path does not exist!')
        return None
    
    def procura_greedy(self, graph, start, end, transport):

        open_list = set([start])
        closed_list = set([])
        order_of_visit = [] #apenas para estatísticas

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

            order_of_visit.append(n)

            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, graph.calcula_custo(reconst_path), order_of_visit)

            # para todos os vizinhos  do nodo corrente
            for (m, edge_attributes) in graph.getNeighbours(n): 
                (weight, is_open, vehicles) = edge_attributes
                if m not in open_list and m not in closed_list and is_open and transport in vehicles: # só considera rua se estiver aberta e veículo puder circular nela
                    open_list.add(m)
                    parents[m] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None
    
    def procura_aStar(self, graph, start, end, transport):

        open_list = {start}
        closed_list = set([])
        order_of_visit = [] #apenas para estatísticas

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[start] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start
        #n = None
        while len(open_list) > 0:

            n = None

            for v in open_list:
                ##if n == None or g[v] + self.getH(v) < g[n] + self.getH(n):  # heuristica ver.....
                if n == None or g[v] + self.calculate_node_heuristic(graph,v,end) < g[n] + self.calculate_node_heuristic(graph,n,end):  # heuristica ver.....
                    n = v
            if n == None:
                print('Cannot deliver package!')
                return None

            order_of_visit.append(n)
            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, graph.calcula_custo(reconst_path), order_of_visit)

            # for all neighbors of the current node do
            for (m, edge_attributes) in graph.getNeighbours(n): # 
                (weight, is_open, vehicles) = edge_attributes
                if m not in open_list and m not in closed_list and is_open and transport in vehicles: # só considera rua se estiver aberta e veículo puder circular nela
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                elif is_open and transport in vehicles:
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