from Package import Package
from datetime import timedelta

# TOCONSIDER: se passar por nodo onde há encomenda, não entrega logo
#               Posso meter a fazer isso, mas quando acrescentarmos delay de entregar (entrega em si demora tempo / cliente pode só querer entrega a partir de x horas depois) pode impedir que se faça entrega no destino final para que se estava a ir
#               Por isso não meti para já pelo menos
class AlgInformed2:

    def add_positions_to_nodes(self,graph,node_positions):
        for location, coords in node_positions.items():
            graph.add_heuristica(location, coords)
            # print("Location: " + location + " (" + str(coords[0]) + "," + str(coords[1]) + ")")
        
    #calcular heurística de nodo baseada em:
    #   dist (pos atual, pos package mais perto) +
    #   diff(tempo atual, tempo limite) (preciso, porque nodos vizinhos podem estar a distância diferente do nodo atual, resultando em tempos diferentes lá) +
    #   diff(tempo inicial, tempo atual) (se estiver muito longe do início, n vale a pena ir lá)
    #   POR CONSIDERAR: diff(tmepo inicial, tempo final) ??
    def calculate_node_heuristic(self, graph, currNode, packages_left, currTime, wantedRating,transport, stats):
        (currX,currY) = graph.get_heuristica(currNode)
        final_res = float('inf') # guardar a heurística mínima, para todos os packages a ser entregues!!
        for package in packages_left.values():
            place = package.m_location
            startTime = package.m_start_time
            endTime = package.m_end_time
            # print(f"package left: {place}, {startTime},{endTime}")
            (endX,endY) = graph.get_heuristica(place)

            # heurística depende de:
            distHeuristic = ((endX-currX)**2 + (endY-currY)**2) # distância (x,y) do ponto atual até um ponto de entrega
            # print (f"GeoDiff {distHeuristic * 100}")

            # diferença de tempo entre tempo atual e prazo inicial de entrega, prejudica se for muito antes do início, não beneficia se for depois
            earlyHeuristic = max(0,(startTime - currTime).total_seconds() / 60)
            # print(f"earlyDiff: {earlyHeuristic * 0.5}") # time diff in minutes

            # diferença de tempo entre tempo atual e prazo máximo de entrega, 
            # prejudica entregas depois do prazo, não beneficia se for antes
            lateHeuristic = max(0,(currTime - endTime).total_seconds() / 60)
            # print(f"lateDiff {lateHeuristic}") # time diff in minutes

            #beneficiar entregas dentro do prazo
            inTimeHeuristic = max(0,(endTime - currTime).total_seconds() / 60)

            speedHeuristic = 0
            if (currNode == package.m_location):
                speedHeuristic = package.m_weight * stats.vel_decr_peso[transport] # aumento de velocidade com entrega de pacote, baseado em peso do pacote
            # print(f"SpeedDiff {-speedHeuristic}") # time diff in minutes

            temp_res = 100 * distHeuristic + lateHeuristic - 1.2 * inTimeHeuristic + 0.25 * earlyHeuristic - 2000 * speedHeuristic
            # - speedHeuristic # heurística para este package
            # print (f"Heuristic iter obtained {temp_res}")

            if (temp_res < final_res):
                final_res = temp_res
        # print ("Heuristic obtained: " + str(final_res))
        return final_res
    
    # decidir qual o melhor transporte de partida, tendo em conta o peso e volume das encomendas
    def get_transport(self, Nodes, stats):
        total_weight = 0
        for Node in Nodes.values():
            total_weight += Node.m_weight
        for transport, weight in stats.max_peso.items():
            if  total_weight <= weight:
                return (transport, total_weight)
        return None
        # se não houver transporte que dê, retorna que não é possível

    # calcular rating para horario em que estafeta entrega pacote
    def calculateRating(self, currTime, location, packages, stats):
        delay = (currTime - packages[location].getEndTime()).total_seconds() / 60 # reduz-se o deliver delay que já foi acrescentado no currTime
        # print (f'Obtained delay: {delay} from endTime: {packages[location].getEndTime().strftime("%Y-%m-%d %H:%M:%S")} and currTime: {currTime.strftime("%Y-%m-%d %H:%M:%S")}')
        for (fixedDelay,rating) in stats.rating_decr_atraso:
            if delay <= fixedDelay:
                return rating
        return 0 # se entrega for depois de 60 minutos é rating 0
    
    # Args:
    #recebe grafo, 
    # nome do nodo inicial, 
    # set de nomes de locais de entrega, 
    def procura_informada(self, graph, startPlace, startTime, wantedRating, packages, node_positions, stats, path_func):

        # atualiza grafo com as posições para cada nodo
        self.add_positions_to_nodes(graph,node_positions)

        result = self.get_transport(packages,stats)
        if not result: # se não houver veículo que consiga transportar todos os pacotes
            print("No vehicle can hold that many packages due to weight/volume")
            return None
        else:
            (transport,total_weight) = result
            print(f"Got transport {transport}") 
            # print(f"with weight {total_weight}")
        
        to_deliver = packages.copy() #pacotes a entregar

        currTime = startTime # tempo inicial
        currVelocity = stats.base_vel[transport] - (total_weight * stats.vel_decr_peso[transport]) # velocidade inicial
        ratings = [] # lista de ratings acumulados de entregas da pacotes
        errorFlag = False
        finalPath = [startPlace]
        totalCost = 0
        currNode = startPlace

        while (len(to_deliver) > 0 and not errorFlag):
            prevNode = currNode # proximo nodo de que se vai partir
            # print("This iteration start: " + prevNode)

            result = path_func(graph,prevNode,to_deliver,startTime, wantedRating, transport, stats)

            if result is not None :
                (path,distTraveled) = result
                # print(f'Got from {path_func.__name__} path: {path} dist: {distTraveled}')

                if (len(path) > 1) : # pode acontecer o primeiro nodo ser logo ponto de entrega e dava mal
                    path.pop(0) # removemos a primeira posição do path obtido, porque já consta na lista final
                finalPath.extend(path) #acrescentar caminho desta iteração ao caminho final
                currNode = path[-1] # próximo nodo em que se começa, aka último nodo a que se chegou na iteração anterior

                totalCost += distTraveled * stats.consumo[transport] # somar C02 na deslocação desta iteração ao total
                timeBetweenDeliveries = timedelta(minutes= (distTraveled / currVelocity)) # tempo decorrido nesta iteração
                # print(f"timeBetweenDeliveries: {timeBetweenDeliveries.total_seconds() / 60}")
                currTime = max(packages[currNode].getStartTime(), currTime + timeBetweenDeliveries) # tempo máximo entre: tempo desde entrega anterior até agora ou tempo inicial de entrega para cliente; + tempo fixo de entregar encomenda
                rating = self.calculateRating(currTime,currNode,packages, stats) # obter rating baseado em tempo de atraso da entrega
                currTime = currTime + timedelta(minutes=stats.deliver_delay) # acrescentar tempo fixo de entrega em qualquer sitio
                ratings.append(rating) # acrescentar rating aos ratings 
                currVelocity += stats.vel_decr_peso[transport] * packages[currNode].getWeight() # aumentar velocidade com redução de peso da entrega

                del to_deliver[currNode] # remover dos pacotes a entregar o pacote atual

            else :
                errorFlag = True

        if (len(to_deliver) == 0 and not errorFlag): # necessário o not errorFlag??
            average_rating = sum(ratings) / len(ratings)

            # print(f'Final CurrTime: {currTime.strftime("%Y-%m-%d %H:%M:%S")}')
            # print(f"Final currVelocity: {currVelocity}")
            # print(f"Final CurrConsumption: {totalCost}")
            # print(f"Final CurrRatings {ratings}")

            return (finalPath,totalCost, average_rating)
        
        print('Path does not exist!')
        return None
    
    def procura_greedy(self, graph, start, to_deliver, currTime, wantedRating, transport, stats):

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
                if n == None or self.calculate_node_heuristic(graph,v,to_deliver,currTime, wantedRating, transport, stats) < self.calculate_node_heuristic(graph,n,to_deliver,currTime, wantedRating, transport, stats):
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
    
    def procura_aStar(self, graph, start, to_deliver, currTime, wantedRating, transport, stats):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = {start}
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {} 

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
                if n == None or g[v] + self.calculate_node_heuristic(graph,v,to_deliver,currTime, wantedRating, transport, stats) < g[n] + self.calculate_node_heuristic(graph,v,to_deliver,currTime, wantedRating, transport, stats): 
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

                        # fatores que afetam o valor de um nodo:
                        # if m in to_deliver:
                        #     g[m] -= to_deliver[m].m_weight * stats.vel_decr_peso[transport] # aumento de velocidade se nodo é ponto de entrega

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None