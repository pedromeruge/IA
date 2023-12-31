from Parser import Parser
from AlgSemiInformed import AlgSemiInformed
from AlgInformed2 import AlgInformed2
from AlgInformed import AlgInformed
from Stats import Stats
from datetime import datetime

def main():
   
    p = Parser()
    # g = p.parseGraph()
    g = p.parseGraphFromOSM("Gualtar")
    package_locations = p.parsePackages()

    # startPos = "Calcada de Cones" # for ParseGraph: encomendas.csv and edges.csv
    # startPos = "Travessa do Bairro" # for ParseGraph: encomendas2.csv and edges2.csv
    startPos = "Rua Monte de Cima" # for ParseGraphFromOSM: encomendas3.csv
    
    startTime = datetime.strptime("2023-12-07 08:00", "%Y-%m-%d %H:%M")

    # # print("Node Coordinates:")
    # # for node, coordinates in node_positions.items():
    # #     print(f"{node}: {coordinates}")

    # # print("Obtained Graph")
    # # for node in g.getNodes():
    # #     print (">>" + str(node))

    # # print("Package Coordinates:")
    # # for package in package_locations.values():
    # #     print ("For location " + package.getLocation() + ",coords: " + str(node_positions[package.getLocation()]))

    # p.drawGraph(20,20, startPos)
    # p.drawGraphFromOSM(20,20,startPos)

    semiInformed = AlgSemiInformed()
    informed = AlgInformed()
    informed2 = AlgInformed2()

    print("Semi-informed BFS search")
    result = semiInformed.procura_informada(g,startPos, startTime, package_locations, semiInformed.procura_BFS)
    if result is not None:
        (path,custo, average_rating, nodesVisited, transport) = result
        print (f"Caminho:\n {len(path)}\nCusto C02 g/km: {custo}, RatingFinal: {average_rating}, NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
        # print (f"Custo C02 g/km: {custo}, RatingFinal: {average_rating}, NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
    else:
        print("Error calculating Semi-informed BFS search") 

    print("Semi-informed DFS search")
    result = semiInformed.procura_informada(g,startPos, startTime, package_locations, semiInformed.procura_DFS)
    if result is not None:
        (path,custo, average_rating, nodesVisited, transport) = result
        print (f"Caminho:\n {len(path)}\nCusto C02 g/km: {custo}, RatingFinal: {average_rating}, NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
        # print (f"Custo C02 g/km: {custo}, RatingFinal: {average_rating}, NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
    else:
        print("Error calculating Semi-informed DFS search") 
        
    print("Semi-informed UCS search")
    result = semiInformed.procura_informada(g,startPos, startTime, package_locations, semiInformed.procura_UCS)
    if result is not None:
        (path,custo, average_rating, nodesVisited, transport) = result
        print (f"Caminho:\n {len(path)}\nCusto C02 g/km: {custo}, RatingFinal: {average_rating}, NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
        # print (f"Custo C02 g/km: {custo}, RatingFinal: {average_rating}, NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
    else:
        print("Error calculating Semi-informed UCS search") 
        
    print("Bad informed greedy search")
    result = informed.procura_informada(g,startPos, startTime, package_locations, informed.procura_greedy)
    if result is not None:
        (path,custo, avg_rating, nodesVisited, transport) = result
        print (f"Caminho:\n {len(path)}\nCusto C02 g/km: {custo}, RatingFinal: {avg_rating},  NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
        # print (f"Custo C02 g/km: {custo}, RatingFinal: {avg_rating}, NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
    else:
        print("Error calculating Bad informed greedy search") 

    print("Bad informed aStar search")
    result = informed.procura_informada(g,startPos, startTime, package_locations, informed.procura_aStar)
    if result is not None:
        (path,custo, avg_rating, nodesVisited, transport) = result
        print (f"Caminho:\n {len(path)}\nCusto C02 g/km: {custo}, RatingFinal: {avg_rating},  NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
        # print (f"Custo C02 g/km: {custo}, RatingFinal: {avg_rating}, NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
    else:
        print("Error calculating Bad informed aStar search") 

    print("Informed greedy search")
    result = informed2.procura_informada(g,startPos, startTime, package_locations, informed2.procura_greedy)
    if result is not None:
        (path,custo, avg_rating, nodesVisited, transport) = result
        print (f"Caminho:\n {len(path)}\nCusto C02 g/km: {custo}, RatingFinal: {avg_rating},  NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
        # print (f"Custo C02 g/km: {custo}, RatingFinal: {avg_rating}, NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
    else:
        print("Error calculating Informed greedy search") 

    print("Informed aStar search")
    result = informed2.procura_informada(g,startPos, startTime, package_locations, informed2.procura_aStar)
    if result is not None:
        (path,custo, avg_rating, nodesVisited, transport) = result
        print (f"Caminho: {len(path)}\n {path}\nCusto C02 g/km: {custo}, RatingFinal: {avg_rating},  NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
        # print (f"Custo C02 g/km: {custo}, RatingFinal: {avg_rating}, NodesVisited {len(nodesVisited)}, BestTransport: {transport}")
    else:
        print("Error calculating Informed aStar search") 

if __name__ == "__main__":
    main()