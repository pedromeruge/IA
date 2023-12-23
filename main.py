from Parser import Parser
from AlgInformed2 import AlgInformed2

def main():
   
    p = Parser()
    g = p.parseGraph()
    package_locations = p.parsePackages()
    node_positions = p.getNodePositions()

    startPos = "Largo da Madre de Deus"
    # print("Node Coordinates:")
    # for node, coordinates in node_positions.items():
    #     print(f"{node}: {coordinates}")

    # print("Obtained Graph")
    # for node in g.getNodes():
    #     print (">>" + str(node))

    p.drawGraph(20,20, startPos)


    print("Package Coordinates:")
    for package in package_locations.values():
        node = g.get_node_by_name(package.getLocation())
        print ("For location " + package.getLocation() + ",coords: " + str(node_positions[node.getName()]))
    

    informed2 = AlgInformed2()

    result = informed2.procura_informada(g,startPos,package_locations, node_positions, informed2.procura_aStar)
    if result is not None:
        (path,custo) = result
        print (path)
        print (custo)
    else:
        print("Error calculating informed") 

if __name__ == "__main__":
    main()