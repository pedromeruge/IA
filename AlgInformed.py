from Graph import Graph
from Node import Node
from Package import Package

# TOCONSIDER: se passar por nodo onde há encomenda, não entrega logo
#               Posso meter a fazer isso, mas quando acrescentarmos delay de entregar pode impedir que se faça entrega no destino pretendido,
#               Por isso não meti para já pelo menos
class AlgInformed:
    def __init__(self):
        print("Calculating Informed")

    # retorna set ordenado com ordem de visita de packages, baseada no tempo limite de entrega mais próximo
    def calculate_heuristic_urgency(self, graph, packages):
        node_visit_order = []
        sorted_packages = sorted(packages, key=Package.getEndTime) # sort packages by delivery urgency
        for package in sorted_packages:
            n1 = graph.get_node_by_name(package.getLocation())
            node_visit_order.append(n1)
        return node_visit_order
    
    def add_positions_to_nodes(self,graph,node_positions):
        for (location,x,y) in node_positions:
            graph.add_heuristica(location,(x,y))
            print ("Location: " + location + " (" + str(x) + "," + str(y) + ")")
        
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
     # tempo atual
    def procura_greedy(self, graph, start, packages, node_positions):
        
        # lista com nodos por visitar, ordenado por proximidade de data limite
        node_visit_order = self.calculate_heuristic_urgency(graph,packages)
        for node in node_visit_order:
            print (node)

        # atualiza grafo com as posições para cada nodo
        self.add_positions_to_nodes(graph,node_positions)

        errorFlag = False
        finalPath = [start]
        totalCost = 0
        next = Node(start)

        while len(node_visit_order) > 0 and not errorFlag:
            # print("Array before iteration decision: ")
            # for node in node_visit_order:
            #     print(node)
            prev = next
            next = node_visit_order.pop(0)
            # print("This iteration start: " + prev.getName() + ", end: " + next.getName())
            # print("Searching for path between " + prev.getName() + " and " + next.getName())
            result = self.procura_greedy_Aux(graph,prev.getName(),next.getName())
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
    
    def procura_greedy_Aux(self, graph, start, end):
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
            prev = n 
            # encontra nodo com a menor heuristica
            for v in open_list:

                # distancia em relação ao próximo nodo a visitar
                if n == None or self.calculate_node_heuristic(graph,v,end) < self.calculate_node_heuristic(graph,n,end):
                    n = v
                # se prazo igual, desempatar com menor distância

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