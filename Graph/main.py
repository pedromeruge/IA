import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def main():
    csv_file_path = 'Graph/edges.csv'
    df = pd.read_csv(csv_file_path)

    G = nx.Graph()

    for index, row in df.iterrows():
        node1, node2, weight = row['Node1'], row['Node2'], row['Weight']
        if G.has_edge(node1, node2):
            G[node1][node2]['weight'] += weight
        else:
            G.add_edge(node1, node2, weight=weight)

    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())

    pos = nx.spring_layout(G, seed=42)
    node_size = 10
    edge_width = 0.5
    edge_color = 'gray'

    plt.figure(figsize=(15, 15))
    nx.draw(G, pos, with_labels=True, node_size=node_size, width=edge_width, edge_color=edge_color)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

if __name__ == "__main__":
    main()