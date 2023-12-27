import osmnx as ox
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
        self.m_encomendas = None
 
    #map location -> package 
    # NOTE: package also includes location, but easier to acess like this
    def parsePackages(self):
        csv_file_path = 'Graph/encomendas3.csv'
        df = pd.read_csv(csv_file_path)
        encomendas_map = {}

        for index, row in df.iterrows():
            rua = row['Rua'].strip()
            package = Package(rua,row['Peso(kg)'], row['Volume(cm^3)'], row['StartDate'].strip(), row['EndDate'].strip())
            encomendas_map[rua] = package

        self.m_encomendas = encomendas_map
        return encomendas_map

    def parseGraph(self):
        csv_file_path = 'Graph/edges2.csv'
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
        # self.m_pos = nx.spring_layout(G, seed=42, weight='weight')
        self.m_pos = nx.kamada_kawai_layout(G, weight='weight')
        # self.m_pos = nx.fruchterman_reingold_layout(G, weight='weight')

        return my_graph
    
    def parseGraphFromOSM(self, location_name, network_type="drive"):
        map_graph = ox.graph_from_place(location_name, network_type=network_type)

        my_graph = Graph()
        G = nx.Graph()
        i = 0
        for edge in map_graph.edges(data=True):
            node1, node2, data = edge
            street_name = data.get("name", "?" + str(i))

            weight = data['length']
            x1, y1 = (map_graph.nodes[node1]['x'], map_graph.nodes[node1]['y'])
            x2, y2 = (map_graph.nodes[node2]['x'], map_graph.nodes[node2]['y'])
            middle_node = str(self.get_first_element(street_name))

            if middle_node.find("?") >= 0: # utilizado para ter nomes diferentes nas ruas todas
                i = i+1

            # criamos um novo ponto intermedio, com o nome da rua
            x3, y3 = (x1+x2)/2, (y1+y2)/2
            node1_name = str(node1)
            node2_name = str(node2)

            # print (f"node1: {node1_name}, node2: {node2_name}")
            if G.has_edge(node1_name, middle_node):
                G[node1_name][middle_node]['weight'] += weight/2
            else:
                G.add_edge(node1_name, middle_node, weight=weight/2)

            if G.has_edge(middle_node, node2_name):
                G[middle_node][node2_name]['weight'] += weight/2
            else:
                G.add_edge(middle_node, node2_name, weight=weight/2)
            
            #ler grafo para nossa classe Grafo tambem
            n1 = Node(node1_name)
            n2 = Node(node2_name)
            n3 = Node(middle_node)
            my_graph.add_edge(n1,n3, weight/2)
            my_graph.add_edge(n3,n2, weight/2)
            
            my_graph.add_heuristica(node1_name, (x1,y1))
            my_graph.add_heuristica(node2_name, (x2,y2))
            my_graph.add_heuristica(middle_node, (x3,y3))         

        self.m_G = G

        #layout do grafo a construir
        # self.m_pos = nx.spring_layout(G, seed=42, weight='weight')
        self.m_pos = nx.kamada_kawai_layout(G, weight='weight')
        # self.m_pos = nx.fruchterman_reingold_layout(G, weight='weight')

        print("Finished parsing")
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
        # plt.show()

    #x and y size of window
    # startPos -> nome da posição inicial
    def drawGraphFromOSM(self, xSize, ySize, startPos=None, filename="static_graph.png"):
        if (not self.m_G) or (not self.m_pos) or (not self.m_encomendas):
            print("Must call parseGraph and parsePackages first")
            return None

        node_size = 20
        edge_width = 1
        edge_color = 'gray'

        # desenhar o grafo
        plt.figure(figsize=(xSize, ySize))

        # Draw all nodes without labels
        nx.draw(self.m_G, self.m_pos, with_labels=False, node_size=node_size, width=edge_width, edge_color=edge_color)

        # Draw nodes with labels for those whose names are not integers
        nodes_to_label = [node for node in self.m_pos if not str(node).isdigit()]
        labels = {node: node for node in nodes_to_label}  # Label with the node name itself
        nx.draw_networkx_labels(self.m_G, self.m_pos, labels=labels, font_size=8)

        # Draw edge labels with weights
        edge_labels = {(u, v): f"{data['weight']:.3f}" for u, v, data in self.m_G.edges(data=True)}
        nx.draw_networkx_edge_labels(self.m_G, self.m_pos, edge_labels=edge_labels, font_color='grey', font_size=3)

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
        if startPos:
            if startPos in self.m_pos:
                startPos_pos = self.m_pos[startPos]
                start_circle_radius = 0.6 * len(self.m_G.nodes)  # Adjust the size of the circle around the startPos
                start_circle_color = 'orange'
                nx.draw_networkx_nodes(self.m_G, self.m_pos, nodelist=[startPos], node_size=start_circle_radius,
                                    node_color=start_circle_color, alpha=0.5)

                plt.text(startPos_pos[0], startPos_pos[1] + 0.02, "START",
                        fontsize=10, ha='center', va='center', color='orange')

        plt.savefig(filename, dpi=600)  # guarda grafo em ficheiro para ver depois
        # plt.show()

    def is_valid_integer(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def get_first_element(self, variable):
        if isinstance(variable, list):
            return variable[0] if variable else None
        else:
            return variable