from Parser import Parser
from AlgSemiInformed import AlgSemiInformed
from AlgInformed2 import AlgInformed2
from AlgInformed import AlgInformed
from Stats import Stats
from datetime import datetime

def main():
   
    p = Parser()
    g = p.parseGraph()
    package_locations = p.parsePackages()
    node_positions = p.getNodePositions()

    startPos = "Largo da Madre de Deus"
    startTime = datetime.strptime("2023-12-07 08:00", "%Y-%m-%d %H:%M")
    # print("Node Coordinates:")
    # for node, coordinates in node_positions.items():
    #     print(f"{node}: {coordinates}")

    # print("Obtained Graph")
    # for node in g.getNodes():
    #     print (">>" + str(node))

    #p.drawGraph(20,20, startPos)


    # print("Package Coordinates:")
    # for package in package_locations.values():
    #     node = g.get_node_by_name(package.getLocation())
    #     print ("For location " + package.getLocation() + ",coords: " + str(node_positions[node.getName()]))

    semiInformed = AlgSemiInformed()
    informed = AlgInformed()
    informed2 = AlgInformed2()
    stats = Stats()

    # print("Semi-informed BFS search")
    # result = semiInformed.procura_informada(g,startPos, startTime, package_locations, stats, semiInformed.procura_BFS)
    # if result is not None:
    #     (path,custo, average_rating) = result
    #     print (f"Caminho:\n {path}\nCusto C02 g/km: {custo}, RatingFinal: {average_rating}")
    # else:
    #     print("Error calculating Semi-informed BFS search") 

    # print("Semi-informed DFS search")
    # result = semiInformed.procura_informada(g,startPos, startTime, package_locations, stats, semiInformed.procura_DFS)
    # if result is not None:
    #     (path,custo, average_rating) = result
    #     print (f"Caminho:\n {path}\nCusto C02 g/km: {custo}, RatingFinal: {average_rating}")
    # else:
    #     print("Error calculating Semi-informed DFS search") 

    print("Bad informed greedy search")
    result = informed.procura_informada(g,startPos, startTime, package_locations, node_positions, stats, informed.procura_greedy)
    if result is not None:
        (path,custo, avg_rating) = result
        print (f"Caminho:\n {path}\nCusto C02 g/km: {custo}, RatingFinal: {avg_rating}")
    else:
        print("Error calculating Bad informed greedy search") 

    print("Bad informed aStar search")
    result = informed.procura_informada(g,startPos, startTime, package_locations, node_positions, stats, informed.procura_aStar)
    if result is not None:
        (path,custo, avg_rating) = result
        print (f"Caminho:\n {path}\nCusto C02 g/km: {custo}, RatingFinal: {avg_rating}")
    else:
        print("Error calculating Bad informed aStar search") 

    # print("Informed greedy search")
    # result = informed2.procura_informada(g,startPos, startTime, package_locations, node_positions, stats, informed2.procura_greedy)
    # if result is not None:
    #     (path,custo, average_rating) = result
    #     print (path); print (custo); print (average_rating)
    # else:
    #     print("Error calculating Informed greedy search") 

    # print("Informed aStar search")
    # result = informed2.procura_informada(g,startPos, startTime, package_locations, node_positions, stats, informed2.procura_aStar)
    # if result is not None:
    #     (path,custo) = result
    #     print (path)
    #     print (custo)
    # else:
    #     print("Error calculating Informed aStar search") 

if __name__ == "__main__":
    main()