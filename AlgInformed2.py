import math

from Package import Package
from datetime import timedelta

from Stats import Stats

# TOCONSIDER: se passar por nodo onde há encomenda, não entrega logo
#               Posso meter a fazer isso, mas quando acrescentarmos delay de entregar (entrega em si demora tempo / cliente pode só querer entrega a partir de x horas depois) pode impedir que se faça entrega no destino final para que se estava a ir
#               Por isso não meti para já pelo menos
class AlgInformed2:

    #calcular heurística de nodo baseada em:
    #   dist (pos atual, pos package mais perto) +
    #   diff(tempo inicial, tempo atual) (se estiver muito longe do início, n vale a pena ir lá)
    #   diff(tempo atual, tempo limite) 
    #   speedIncrease
    def calculate_node_heuristic(self, graph, currNode, packages_left, currTime, transport):
        (currX,currY) = graph.get_heuristica(currNode)
        final_res = float('inf') # guardar a heurística mínima, para todos os packages a ser entregues!!
        # print(f"Curr node: {currNode}")

        for package in packages_left.values():
            # print(f"iter for package {package.m_location} ")
            place = package.m_location
            startTime = package.m_start_time
            endTime = package.m_end_time
            # print(f"package left: {place}, {startTime},{endTime}")
            (endX,endY) = graph.get_heuristica(place)

            # heurística depende de:
            distHeuristic = math.sqrt((endX-currX)**2 + (endY-currY)**2) # distância (x,y) do ponto atual até um ponto de entrega
            # print (f"GeoDiff {distHeuristic * 100}")

            # # # diferença de tempo entre tempo atual e prazo inicial de entrega, prejudica se for muito antes do início, não beneficia se for depois
            earlyHeuristic = max(0,(startTime - currTime).total_seconds() / 60)
            # # # print(f"earlyDiff: {earlyHeuristic * 0.25}") # time diff in minutes

            #beneficiar entregas dentro do prazo
            inTimeHeuristic = abs((endTime - currTime).total_seconds() / 60)
            # print(f"timeHeuristic: {inTimeHeuristic}") # time diff in minutes

            speedHeuristic = 0
            if (currNode == package.m_location):
                speedHeuristic = package.m_weight * Stats.vel_decr_peso[transport] # aumento de velocidade com entrega de pacote, baseado em peso do pacote

            temp_res =  ((inTimeHeuristic + earlyHeuristic * 0.2) + 100 * distHeuristic - 2 * speedHeuristic) * 2

            if (temp_res < final_res):
                final_res = temp_res

        return final_res

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
        delay = (currTime - packages[location].getEndTime()).total_seconds() / 60
        # print (f'Obtained delay: {delay} from endTime: {packages[location].getEndTime().strftime("%Y-%m-%d %H:%M:%S")} and currTime: {currTime.strftime("%Y-%m-%d %H:%M:%S")}')
        for (fixedDelay,rating) in Stats.rating_decr_atraso:
            if delay <= fixedDelay:
                return rating
        return 0 # se entrega for depois de 60 minutos é rating 0

    def procura_informada(self, graph, startPlace, startTime, packages, path_func):
        best_path = []
        best_rating = 0
        best_cost = math.inf
        best_nodesVisited = 0
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
                    best_nodesVisited = nodesVisited
                    best_transport = transport

        if best_cost == math.inf:
            return None
        else:
            return (best_path,best_cost,best_rating,best_nodesVisited, best_transport)
        
    def procura_informada_aux(self, graph, startPlace, startTime, packages, transport, total_weight, path_func):

        to_deliver = packages.copy() #pacotes a entregar

        currTime = startTime # tempo inicial
        currVelocity = Stats.base_vel[transport] - (total_weight * Stats.vel_decr_peso[transport]) # velocidade inicial
        ratings = [] # lista de ratings acumulados de entregas da pacotes
        errorFlag = False
        finalPath = [startPlace]
        totalCost = 0
        nodesVisited = set()
        currNode = startPlace

        while (len(to_deliver) > 0 and not errorFlag):
            prevNode = currNode # proximo nodo de que se vai partir
            # print("This iteration start: " + prevNode)

            result = path_func(graph,prevNode,to_deliver,currTime, transport)

            if result is not None :
                (path,distTraveled, visited) = result
                # print(f'Got from {path_func.__name__} path: {path} dist: {distTraveled}')
                nodesVisited = nodesVisited.union(visited)
                currNode = path[-1] # próximo nodo em que se começa, aka último nodo a que se chegou na iteração anterior
                path.pop(0) # removemos a primeira posição do path obtido, porque já consta na lista final
                finalPath.extend(path) #acrescentar caminho desta iteração ao caminho final

                totalCost += distTraveled * Stats.consumo[transport] # somar C02 na deslocação desta iteração ao total
                timeBetweenDeliveries = timedelta(minutes= (distTraveled / currVelocity)) # tempo decorrido nesta iteração
                # print(f"timeBetweenDeliveries: {timeBetweenDeliveries.total_seconds() / 60}")
                currTime = max(packages[currNode].getStartTime(), currTime + timeBetweenDeliveries) # tempo máximo entre: tempo desde entrega anterior até agora ou tempo inicial de entrega para cliente; + tempo fixo de entregar encomenda
                rating = self.calculateRating(currTime,currNode,packages) # obter rating baseado em tempo de atraso da entrega
                currTime = currTime + timedelta(minutes=Stats.deliver_delay) # acrescentar tempo fixo de entrega em qualquer sitio
                ratings.append(rating) # acrescentar rating aos ratings 
                currVelocity += Stats.vel_decr_peso[transport] * packages[currNode].getWeight() # aumentar velocidade com redução de peso da entrega
                # if (transport == "carro"):
                #     print(f'Delivered packet {currNode} with rating {rating} currTime {currTime.strftime("%Y-%m-%d %H:%M:%S")} at pos {graph.get_heuristica(currNode)}')
                del to_deliver[currNode] # remover dos pacotes a entregar o pacote atual

            else :
                errorFlag = True

        if (len(to_deliver) == 0 and not errorFlag): # necessário o not errorFlag??
            average_rating = sum(ratings) / len(ratings)

            # print(f'Final CurrTime: {currTime.strftime("%Y-%m-%d %H:%M:%S")}')
            # print(f"Final currVelocity: {currVelocity}")
            # print(f"Final CurrConsumption: {totalCost}")
            # print(f"Final CurrRatings {ratings}")

            return (finalPath,totalCost, average_rating, nodesVisited)
        
        print('Path does not exist!')
        return None
    
    def procura_greedy(self, graph, start, to_deliver, currTime, transport):

        open_list = set([start])
        closed_list = set([])
        nodesVisited = set() # apenas para estatísticas

        parents = {}
        parents[start] = start

        while len(open_list) > 0:

            n = None

            for v in open_list:

                if n == None or self.calculate_node_heuristic(graph,v,to_deliver,currTime, transport) < self.calculate_node_heuristic(graph,n,to_deliver,currTime, transport):
                    n = v

            if n == None:
                print('Cannot deliver package!')
                return None

            nodesVisited.add(n)
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

                return (reconst_path, graph.calcula_custo(reconst_path), nodesVisited)

            # para todos os vizinhos do nodo corrente
            for (m, edge_attributes) in graph.getNeighbours(n):
                (weight, is_open, vehicles) = edge_attributes
                if m not in open_list and m not in closed_list and is_open and transport in vehicles: # só considera rua se estiver aberta e veículo puder circular nela
                    open_list.add(m)
                    parents[m] = n

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None
    
    def procura_aStar(self, graph, start, to_deliver, currTime, transport):

        open_list = {start}
        closed_list = set([])
        nodesVisited = set() # apenas para estatísticas

        g = {} 

        g[start] = 0

        parents = {}
        parents[start] = start
        #n = None
        while len(open_list) > 0:

            n = None

            for v in open_list:

                if n == None or g[v] + self.calculate_node_heuristic(graph,v,to_deliver,currTime, transport) < g[n] + self.calculate_node_heuristic(graph,n,to_deliver,currTime, transport): 
                    n = v
                    # print(f"Node v {g[v]},{self.calculate_node_heuristic(graph,v,to_deliver,currTime, transport)}, total {g[v] + self.calculate_node_heuristic(graph,v,to_deliver,currTime, transport)}")
                    # print(f"Node n {g[n]},{self.calculate_node_heuristic(graph,n,to_deliver,currTime, transport)}, total {g[n] + self.calculate_node_heuristic(graph,n,to_deliver,currTime, transport)}")
            if n == None:
                print('Cannot deliver package!')
                return None

            nodesVisited.add(n)
            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n in to_deliver:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, graph.calcula_custo(reconst_path), nodesVisited)

            # for all neighbors of the current node do
            for (m, edge_attributes) in graph.getNeighbours(n):
                (weight, is_open, vehicles) = edge_attributes
                if m not in open_list and m not in closed_list and is_open and transport in vehicles: # só considera rua se estiver aberta e veículo puder circular nela
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

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