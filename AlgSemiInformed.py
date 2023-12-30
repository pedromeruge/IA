import math
from queue import Queue
from datetime import datetime, timedelta
from Package import Package
from Stats import Stats

class AlgSemiInformed:

    # heurística baseada em limite de tempo mais proximo
    # retorna lista ordenado com ordem de visita de packages
    def calculate_heuristic_urgency(self, graph, packages):
        node_visit_order = []
        sorted_Nodes = sorted(packages.values(), key=Package.getEndTime) # sort Nodes by delivery urgency
        return sorted_Nodes
    
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
    
    # Args:
    #recebe grafo, 
    # nome do nodo inicial, 
    # lista de pacotes a entregar,
    # funcão de calculo de (custo,path) entre dois nodos -!!- tem de receber como args: grafo, nome inicio, nome final, [], set()

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

        # lista com nodos por visitar, ordenado por proximidade de data limite
        package_visit_order = self.calculate_heuristic_urgency(graph,packages)

        currTime = startTime # tempo inicial
        currVelocity = Stats.base_vel[transport] - (total_weight * Stats.vel_decr_peso[transport]) # velocidade inicial
        ratings = [] # lista de ratings acumulados de entregas da pacotes
        errorFlag = False
        finalPath = [startPlace]
        totalCost = 0
        nodesVisited = set()
        currNode = startPlace

        while (len(package_visit_order) > 0 and not errorFlag):

            prevNode = currNode
            currNode = package_visit_order.pop(0).getLocation() # procurar nodo com encomenda mais urgente da lista

            # print(f"This iteration start: from {prevNode} to {currNode}")
            # print(f'CurrTime: {currTime.strftime("%Y-%m-%d %H:%M:%S")}')
            # print(f"currVelocity: {currVelocity}")
            # print(f"CurrConsumption: {totalCost}")
            # print(f"CurrRatings {ratings}")

            result = path_func(graph,prevNode,currNode, transport)
            if result is not None :
                (path,distTraveled, visited) = result 
                # print(f'Got from {path_func.__name__} path: {path} dist: {distTraveled}')

                path.pop(0) # removemos a primeira posição do path obtido, porque já consta na lista final
                finalPath.extend(path) # acrescentar caminho desta iteração ao caminho final
                totalCost += distTraveled * Stats.consumo[transport] # somar C02 na deslocação desta iteração ao total
                nodesVisited = nodesVisited.union(visited) # nodos visitados nessa iteração
                
                timeBetweenDeliveries = timedelta(minutes= (distTraveled / currVelocity)) # tempo decorrido nesta iteração
                # print(f"timeBetweenDeliveries: {timeBetweenDeliveries.total_seconds() / 60}")
                currTime = max(packages[currNode].getStartTime(), currTime + timeBetweenDeliveries) # tempo máximo entre: tempo desde entrega anterior até agora ou tempo inicial de entrega para cliente; + tempo fixo de entregar encomenda
                rating = self.calculateRating(currTime,currNode,packages) # obter rating baseado em tempo de atraso da entrega
                currTime = currTime + timedelta(minutes=Stats.deliver_delay) # acrescentar tempo fixo de entrega em qualquer sitio
                ratings.append(rating) # acrescentar rating aos ratings 
                currVelocity += Stats.vel_decr_peso[transport] * packages[currNode].getWeight() # aumentar velocidade com redução de peso da entrega

            else :
                errorFlag = True

        if (len(package_visit_order) == 0 and not errorFlag): # necessário o not errorFlag??
            average_rating = sum(ratings) / len(ratings)

            # print(f'Final CurrTime: {currTime.strftime("%Y-%m-%d %H:%M:%S")}')
            # print(f"Final currVelocity: {currVelocity}")
            # print(f"Final CurrConsumption: {totalCost}")
            # print(f"Final CurrRatings {ratings}")

            return (finalPath,totalCost, average_rating, nodesVisited)
        
        return None
    
    def procura_BFS(self, graph, start, end, transport):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()
        custo = 0
        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        # garantir que o start node nao tem pais...
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, edge_attributes) in graph.getSpecificNode(nodo_atual):
                    (dist, is_open, vehicles) = edge_attributes
                    if adjacente not in visited and is_open and transport in vehicles: # só considera vizinhos se estrada de ligação está aberta e pode circular esse veículo
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)

        # reconstruir o caminho

        if path_found:
            path = []
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # funçao calcula custo caminho
            custo = graph.calcula_custo(path)
            return (path, custo, visited)

        return None

    def procura_DFS_call(self, graph, start,end, transport, path=[], visited=set()):
        path.append(start) #caminho até ao destino
        visited.add(start) # nodos vistados

        if start == end: #chegou ao destino
            #calcular o custo do caminho função calcula custo
            custoT = graph.calcula_custo(path)
            return (path,custoT, visited)
        
        for (adjacente, edge_attributes) in graph.getSpecificNode(start):
            (dist, is_open, vehicles) = edge_attributes
            if adjacente not in visited and is_open and transport in vehicles:
                resultado = self.procura_DFS_call(graph, adjacente, end, transport, path, visited)
                if resultado is not None:
                    return resultado
        path.pop() # se não encontrar remover o que está no caminho
        return None
    
    def procura_DFS(self,graph,start,end, transport):
        return self.procura_DFS_call(graph,start,end, transport, [], set())

