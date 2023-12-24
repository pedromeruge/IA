from Graph import Graph
from Node import Node
from Package import Package
from AlgSemiInformed import AlgSemiInformed
from AlgNonInformed import AlgNonInformed
from AlgInformed import AlgInformed
from AlgInformed2 import AlgInformed2
import random

def main():
    elvas = Node("elvas")
    estremoz = Node("estremoz")
    evora = Node("evora")
    borba = Node("borba")
    anturas = Node("anturas")

    p1 = Package("estremoz","2023-12-07 09:00","2023-12-07 09:30")
    p2 = Package("evora","2023-12-07 09:00","2023-12-07 09:30")
    p3 = Package("borba","2023-12-07 09:00","2023-12-07 09:45")
    p4 = Package("anturas","2023-12-07 09:00","2023-12-07 09:35")

    g = Graph()

    g.add_edge(elvas,estremoz,2)
    g.add_edge(elvas, borba, 3)
    g.add_edge(elvas,evora,1)
    g.add_edge(estremoz, anturas, 4)
    g.add_edge(evora, anturas, 5)
    g.add_edge(estremoz,borba,2)
    g.add_edge(evora,borba,2)

    packages_locations = [p1,p2,p3,p4]

    ####### procura informada 2 ###########
    node_positions = {}
    node_positions["elvas"] = (5,10)
    node_positions["estremoz"] = (5,8)
    node_positions["anturas"] = (5,2)
    node_positions["evora"] = (4,9)
    node_positions["borba"] = (6,7)

    informed2 = AlgInformed2()

    packages = {package.m_location: package for package in packages_locations} # map dos pacotes a entregar, location para respetivo pacote (acessos rápidos)
        
    result = informed2.procura_informada(g,"elvas",packages, node_positions, informed2.procura_aStar)
    if result is not None:
        (path,custo) = result
        print (path)
        print (custo)
    else:
        print("Error calculating informed") 

if __name__ == "__main__":
    main()