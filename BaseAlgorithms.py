from Graph import Graph 
from Node import Node
from Package import Package
from queue import Queue
import heapq

class BaseAlgorithms:
    def __init__(self):
        None

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
