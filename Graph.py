
import math
from Stats import Stats
from Node import Node


# Constructor
# Methods for adding edges
# Methods for removing edges
# Methods for searching a graph
# BFS, DFS
# Other interesting methods


class Graph:

    def __init__(self, directed=False):
        self.m_nodes = [] # lista de todos os nodos do grafo
        self.m_directed = directed
        self.m_graph = {}  # dicionario para armazenar os nodos e arestas
        self.m_h = {} # dicionario para armazenar as heuristicas para cada nodo -< pesquisa informada
    #############
    #    escrever o grafo como string
    #############
    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node" + str(key) + ": " + str(self.m_graph[key]) + "\n"
        return out

    ################################
    #   encontrar nodo pelo nome
    ################################

    def get_node_by_name(self, name):
        search_node = Node(name)
        for node in self.m_nodes:
            if node == search_node:
                return node
        return None

    #   imprimir arestas
    def imprime_aresta(self):
        listaA = ""
        lista = self.m_graph.keys()
        for nodo in lista:
            for (nodo2, custo) in self.m_graph[nodo]:
                listaA = listaA + nodo + " ->" + nodo2 + " custo:" + str(custo) + "\n"
        return listaA

    #   adicionar   aresta no grafo
    
    # dist is distance between nodes
    def add_edge(self, n1, n2, dist, is_open=True, vehicles=Stats.transportes):
        node1 = n1.getName()
        node2 = n2.getName()

        if (n1 not in self.m_nodes):
            n1_id = len(self.m_nodes)  # numeração sequencial
            n1.setId(n1_id)
            self.m_nodes.append(n1)
            self.m_graph[node1] = []

        if (n2 not in self.m_nodes):
            n2_id = len(self.m_nodes)  # numeração sequencial
            n2.setId(n2_id)
            self.m_nodes.append(n2)
            self.m_graph[node2] = []

        # distance of edge, is road open, vehicles allowed in this road
        edge_attributes = (dist, is_open, vehicles)
        self.m_graph[node1].append((node2, edge_attributes))  # poderia ser n1 para trabalhar com nodos no grafo

        if not self.m_directed:
              self.m_graph[node2].append((node1, edge_attributes))

    def add_heuristica(self, n, valor):
        n1 = Node(n)
        if n1 in self.m_nodes:
            self.m_h[n] = valor

    def get_heuristica(self,n):
        return self.m_h[n]
    
    def getSpecificNode(self,name):
        return self.m_graph[name]
    
    # devolver nodos
    def getNodes(self):
        return self.m_nodes

    def getNumberOfNodes(self):
        return len(self.m_nodes)
    
    def getNeighbours(self,n):
        neighbours = []
        node = Node(n)
        if node in self.m_nodes:
            neighbours = self.m_graph[n]
        return neighbours

    #    devolver o custo de uma aresta
    def get_arc_cost(self, node1, node2):
        custoT = math.inf
        a = self.m_graph[node1]  # lista de arestas para aquele nodo
        for (nodo, edge_attributes) in a:
            (custo,_,_) = edge_attributes
            if nodo == node2:
                custoT = custo
        return custoT

    #  dado um caminho calcula o seu custo
    def calcula_custo(self, caminho):
        # caminho é uma lista de nodos
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            i = i + 1
        return custo