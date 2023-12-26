from Package import Package
from datetime import timedelta

# TOCONSIDER: se passar por nodo onde há encomenda, não entrega logo
#               Posso meter a fazer isso, mas quando acrescentarmos delay de entregar (entrega em si demora tempo / cliente pode só querer entrega a partir de x horas depois) pode impedir que se faça entrega no destino final para que se estava a ir
#               Por isso não meti para já pelo menos
class AlgInformed:

    # heurística baseada em limite de tempo mais proximo
    # retorna lista ordenado com ordem de visita de packages
    def calculate_heuristic_urgency(self, graph, packages):
        node_visit_order = []
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
        res = ((endX-currX)**2 + (endY-currY)**2)
        return res
    
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
    def procura_informada(self, graph, startPlace, startTime, packages, node_positions, stats, path_func):
        
        # lista com nodos por visitar, ordenado por proximidade de data limite
        package_visit_order = self.calculate_heuristic_urgency(graph,packages)

        # atualiza grafo com as posições para cada nodo
        self.add_positions_to_nodes(graph,node_positions)

        #obter transporte adequado (para peso e volume)
        result = self.get_transport(packages,stats)
        if not result: # se não houver veículo que consiga transportar todos os pacotes
            print("No vehicle can hold that many packages due to weight/volume")
            return None
        else:
            (transport,total_weight) = result
            print(f"Got transport {transport}") 
            # print(f"with weight {total_weight}")
        
        currTime = startTime # tempo inicial
        currVelocity = stats.base_vel[transport] - (total_weight * stats.vel_decr_peso[transport]) # velocidade inicial
        ratings = [] # lista de ratings acumulados de entregas da pacotes
        errorFlag = False
        finalPath = [startPlace]
        totalCost = 0
        currNode = startPlace

        while len(package_visit_order) > 0 and not errorFlag:
            # print("Array before iteration decision: ")
            # for node in node_visit_order:
            #     print(node)
            prevNode = currNode
            currNode = package_visit_order.pop(0).getLocation() # procurar nodo com encomenda mais urgente da lista

            result = path_func(graph,prevNode,currNode)
            if result is not None :
                (path,distTraveled) = result 
                # print(f'Got from {path_func.__name__} path: {path} dist: {distTraveled}')

                path.pop(0) # removemos a primeira posição do path obtido, porque já consta na lista final
                finalPath.extend(path) # acrescentar caminho desta iteração ao caminho final
                totalCost += distTraveled * stats.consumo[transport] # somar C02 na deslocação desta iteração ao total
                timeBetweenDeliveries = timedelta(minutes= (distTraveled / currVelocity)) # tempo decorrido nesta iteração
                # print(f"timeBetweenDeliveries: {timeBetweenDeliveries.total_seconds() / 60}")
                currTime = max(packages[currNode].getStartTime(), currTime + timeBetweenDeliveries) # tempo máximo entre: tempo desde entrega anterior até agora ou tempo inicial de entrega para cliente; + tempo fixo de entregar encomenda
                rating = self.calculateRating(currTime,currNode,packages, stats) # obter rating baseado em tempo de atraso da entrega
                currTime = currTime + timedelta(minutes=stats.deliver_delay) # acrescentar tempo fixo de entrega em qualquer sitio
                ratings.append(rating) # acrescentar rating aos ratings 
                currVelocity += stats.vel_decr_peso[transport] * packages[currNode].getWeight() # aumentar velocidade com redução de peso da entrega

            else :
                errorFlag = True

        if (len(package_visit_order) == 0) and not errorFlag: # necessário o not errorFlag??
            average_rating = sum(ratings) / len(ratings)

            # print(f'Final CurrTime: {currTime.strftime("%Y-%m-%d %H:%M:%S")}')
            # print(f"Final currVelocity: {currVelocity}")
            # print(f"Final CurrConsumption: {totalCost}")
            # print(f"Final CurrRatings {ratings}")

            return (finalPath,totalCost, average_rating)

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