import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from Parser import Parser

def main():
   
    p = Parser()
    my_graph = p.parseGraph()
    node_positions = p.getNodePositions()

    print("Node Coordinates:")
    for node, coordinates in node_positions.items():
        print(f"{node}: {coordinates}")

    # p.drawGraph(10,8)

    package_locations = p.parsePackages()
    
    print("Node Coordinates:")
    for package in package_locations.values():
        print(package)

    # informed2 = AlgInformed2()
    # result = informed2.procura_informada(g,"elvas",packages_locations, node_positions, informed2.procura_aStar)
    # if result is not None:
    #     (path,custo) = result
    #     print (path)
    #     print (custo)
    # else:
    #     print("Error calculating informed") 

if __name__ == "__main__":
    main()