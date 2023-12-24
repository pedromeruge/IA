from asyncio import Queue
from Graph import Graph 
from Node import Node
from Node import Node
from queue import Queue
from datetime import datetime, timedelta
from Package import Package

class AlgSemiInformed:

    # devolve map que associa a cada nodo heurística baseada em limite de tempo mais proximo
    # Args:
    # 
    def calculate_heuristic_urgency(self, graph, packages):
        node_visit_order = []
        sorted_Nodes = sorted(packages.values(), key=Package.getEndTime) # sort Nodes by delivery urgency
        return sorted_Nodes
    
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
    # lista de pacotes a entregar,
    # funcão de calculo de (custo,path) entre dois nodos -!!- tem de receber como args: grafo, nome inicio, nome final, [], set()

    def procura_informada(self, graph, startPlace, startTime, packages, node_positions, stats, path_func):

        # lista com nodos por visitar, ordenado por proximidade de data limite
        Package_visit_order = self.calculate_heuristic_urgency(graph,packages)

        (transport,total_weight) = self.get_transport(packages,stats)
        if not transport: # se não houver veículo que consiga transportar todos os pacotes
            print("No vehicle can hold that many Nodes due to weight/volume")
            return None
        else:
            print(f"Got transport {transport}") 
            # print(f"with weight {total_weight}")
        
        currTime = startTime # tempo inicial
        currVelocity = stats.base_vel[transport] - (total_weight * stats.vel_decr_peso[transport]) # velocidade inicial
        ratings = [] # lista de ratings acumulados de entregas da pacotes
        errorFlag = False
        finalPath = [startPlace]
        totalCost = 0
        currNode = startPlace

        while len(Package_visit_order) > 0 and not errorFlag:

            prevNode = currNode
            currNode = Package_visit_order.pop(0).getLocation() # procurar nodo com encomenda mais urgente da lista

            # print(f"This iteration start: from {prevNode} to {currNode}")
            # print(f'CurrTime: {currTime.strftime("%Y-%m-%d %H:%M:%S")}')
            # print(f"currVelocity: {currVelocity}")
            # print(f"CurrConsumption: {totalCost}")
            # print(f"CurrRatings {ratings}")

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

        if (len(Package_visit_order) == 0) and not errorFlag: # necessário o not errorFlag??
            average_rating = sum(ratings) / len(ratings)

            # print(f'Final CurrTime: {currTime.strftime("%Y-%m-%d %H:%M:%S")}')
            # print(f"Final currVelocity: {currVelocity}")
            # print(f"Final CurrConsumption: {totalCost}")
            # print(f"Final CurrRatings {ratings}")

            return (finalPath,totalCost, average_rating)
        
        print('Path does not exist!')
        return None
    
    def procura_BFS(self, graph, start, end):
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
                for (adjacente, peso) in graph.getSpecificNode(nodo_atual):
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)

        # reconstruir o caminho

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # funçao calcula custo caminho
            custo = graph.calcula_custo(path)
        return (path, custo)

    def procura_DFS_call(self, graph, start,end,path=[],visited=set()):
        path.append(start) #caminho até ao destino
        visited.add(start) # nodos vistados
        #print("visted: " + str(start))
        # print(visited)

        if start == end: #chegou ao destino
            #calcular o custo do caminho função calcula custo
            custoT = graph.calcula_custo(path)
            return (path,custoT)
        
        for (adjacente, peso) in graph.getSpecificNode(start):
            if adjacente not in visited:
                resultado = self.procura_DFS_call(graph, adjacente, end, path, visited)
                if resultado is not None:
                    return resultado
        path.pop() # se não encontrar remover o que está no caminho
        return None
    
    def procura_DFS(self,graph,start,end):
        return self.procura_DFS_call(graph,start,end,[],set())

    def procura_uniforme(self, graph, start, end):
        return None
