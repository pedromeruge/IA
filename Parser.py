import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from Graph import Graph
from Node import Node
from Package import Package
from datetime import datetime

class Parser:
    def __init__(self):
        self.m_G = None
        self.m_pos = None
        self.m_encomendas = None
 
    #map location -> package 
    # NOTE: package also includes location, but easier to acess like this
    def parsePackages(self):
        csv_file_path = 'Graph/encomendas.csv'
        df = pd.read_csv(csv_file_path)
        encomendas_map = {}

        for index, row in df.iterrows():
            rua = row['Rua'].strip()
            package = Package(rua,row['Peso(kg)'], row['Volume(cm^3)'], row['StartDate'].strip(), row['EndDate'].strip())
            encomendas_map[rua] = package

        self.m_encomendas = encomendas_map
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
            node1, node2, weight = row['Node1'].strip(), row['Node2'].strip(), row['Weight']
            #ler grafo para biblioteca  networkx
            if G.has_edge(node1, node2):
                G[node1][node2]['weight'] += weight
            else:
                G.add_edge(node1, node2, weight=weight)
            
            #ler grafo para nossa classe Grafo tambem
            n1 = Node(node1)
            n2 = Node(node2)
            my_graph.add_edge(n1,n2, weight)

        # print("Number of nodes:", G.number_of_nodes())
        # print("Number of edges:", G.number_of_edges())

        #guardar Grafo lido de ficheiro
        self.m_G = G

        #layout do grafo a construir
        self.m_pos = nx.spring_layout(G, seed=42, weight='weight')
        #self.m_pos = nx.kamada_kawai_layout(G, weight='weight')

        return my_graph
        
    def getNodePositions(self):
        if (not self.m_G) or (not self.m_pos):
            print ("must call parseGraph first")
        #map de: localizacao -> (x,y)
        node_positions = {node: self.m_pos[node] for node in self.m_G.nodes}
        return node_positions
    
    #x and y size of window
    # startPos -> nome da posição inicial
    def drawGraph(self, xSize, ySize, startPos = None, filename = "static_graph.png"):
        if (not self.m_G) or (not self.m_pos) or (not self.m_encomendas):
            print ("Must call parseGraph and parsePackages first")
            return None
        
        node_size = 20
        edge_width = 1
        edge_color = 'gray'

        # desenhar o grafo
        plt.figure(figsize=(xSize, ySize))
        nx.draw(self.m_G, self.m_pos, with_labels=True, node_size=node_size, width=edge_width, edge_color=edge_color)
        labels = nx.get_edge_attributes(self.m_G, 'weight')
        nx.draw_networkx_edge_labels(self.m_G, self.m_pos, edge_labels=labels)

        # Desenhar circulos à volta de todos os nodos e as datas de fim e início
        for node, pos in self.m_pos.items():
            if node in self.m_encomendas:
                    encomenda = self.m_encomendas[node]
                    circle_radius = 0.6 * len(self.m_G.nodes)
                    circle_color = 'red'
                    nx.draw_networkx_nodes(self.m_G, self.m_pos, nodelist=[node], node_size=circle_radius,
                                        node_color=circle_color, alpha=0.5)

                    # Annotate with delivery information
                    dateStart = encomenda.getStartTime().strftime("%Y-%m-%d %H:%M:%S")
                    dateEnd = encomenda.getEndTime().strftime("%Y-%m-%d %H:%M:%S")
                    plt.text(pos[0], pos[1] + 0.02, f"Begin: {dateStart}\nEnd: {dateEnd}",
                            fontsize=8, ha='center', va='center', color='red')
    
        # Desenhar circulo à volta da posicao inicial
        if startPos :
            if startPos in self.m_pos:
                startPos_pos = self.m_pos[startPos]
                start_circle_radius = 0.6 * len(self.m_G.nodes)  # Adjust the size of the circle around the startPos
                start_circle_color = 'orange'
                nx.draw_networkx_nodes(self.m_G, self.m_pos, nodelist=[startPos], node_size=start_circle_radius,
                                    node_color=start_circle_color, alpha=0.5)

                plt.text(startPos_pos[0], startPos_pos[1] + 0.02, "START",
                        fontsize=10, ha='center', va='center', color='orange')

        plt.savefig(filename, dpi=600) # guarda grafo em ficheiro para ver depois
        #plt.show()

