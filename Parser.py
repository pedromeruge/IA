import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from Graph import Graph
from Node import Node
from Package import Package

class Parser:
    def __init__(self):
        self.m_G = None
        self.m_pos = None
 
    #map location -> package 
    # NOTE: package also includes location, but easier to acess like this
    def parsePackages(self):
        csv_file_path = 'Graph/encomendas.csv'
        df = pd.read_csv(csv_file_path)
        encomendas_map = {}

        for index, row in df.iterrows():
            rua = row['Rua']
            package = Package(rua,row['Peso(kg)'], row['Volume(cm^3)'], row['StartDate'], row['EndDate'])
            encomendas_map[rua] = package

        return encomendas_map

    #reading edges from csv file
        #internally stores graph info for plotting and getting node coordinates
        #returns graph of Graph class
    def parseGraph(self):
        csv_file_path = 'Graph/edges.csv'
        df = pd.read_csv(csv_file_path)

        G = nx.Graph()
        my_graph = Graph()

        # ler grafo de ficheiro
        for index, row in df.iterrows():
            node1, node2, weight = row['Node1'], row['Node2'], row['Weight']
            #ler grafo para biblioteca  networkx
            if G.has_edge(node1, node2):
                G[node1][node2]['weight'] += weight
            else:
                G.add_edge(node1, node2, weight=weight)
            
            #ler grafo para nossa classe Grafo tambem
            n1 = Node(node1)
            n2 = Node(node2)
            my_graph.add_edge(n1,n2, weight)

        print("Number of nodes:", G.number_of_nodes())
        print("Number of edges:", G.number_of_edges())

        #guardar Grafo lido de ficheiro
        self.m_G = G

        #layout do grafo a construir
        self.m_pos = nx.spring_layout(G, seed=42)

        return my_graph
        
    def getNodePositions(self):
        if (not self.m_G) or (not self.m_pos):
            print ("must call parseGraph first")
        #map de: localizacao -> (x,y)
        node_positions = {node: self.m_pos[node] for node in self.m_G.nodes}
        return node_positions
    
    #x and y size of window
    def drawGraph(self, xSize, ySize):
        if (not self.m_G) or (not self.m_pos):
            print ("Must call parseGraph first")
            return None
        
        node_size = 10
        edge_width = 0.5
        edge_color = 'gray'

        # desenhar o grafo
        plt.figure(figsize=(xSize, ySize))
        nx.draw(self.m_G, self.m_pos, with_labels=True, node_size=node_size, width=edge_width, edge_color=edge_color)
        labels = nx.get_edge_attributes(self.m_G, 'weight')
        nx.draw_networkx_edge_labels(self.m_G, self.m_pos, edge_labels=labels)
        plt.show()

