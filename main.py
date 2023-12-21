from Graph import Graph
from Node import Node
from Algorithms import Algorithms

def main():
    elvas = Node("elvas")
    estremoz = Node("estremoz","2023-12-07 09:00","2023-12-07 09:30")
    evora = Node("evora","2023-12-07 09:00","2023-12-07 09:30")
    borba = Node("borba","2023-12-07 09:00","2023-12-07 09:45")
    anturas = Node("anturas","2023-12-07 09:00","2023-12-07 09:35")

    g = Graph()

    g.add_edge(elvas,estremoz,2)
    g.add_edge(elvas, borba, 3)
    g.add_edge(elvas,evora,1)
    g.add_edge(estremoz, anturas, 4)
    g.add_edge(evora, anturas, 5)
    g.add_edge(estremoz,borba,2)
    g.add_edge(evora,borba,2)

    a = Algorithms()

    #delivery_locations = {"elvas","estremoz","evora","borba","anturas"}

    #(path, custo) = a.greedy_tsp_with_timeframes(g,"elvas",delivery_locations)

    #print (path)
    
    goals = {"estremoz","evora","borba","anturas"}
    
    resultDFS = a.procura_DFS(g,"elvas",goals)
    print (f'DFS: {resultDFS}')
    
    resultBFS = a.procura_BFS(g,"elvas",goals)
    print (f'BFS: {resultBFS}')
    
    resultUniforme = a.procura_Uniforme(g,"elvas",goals)
    print (f'Uniforme: {resultUniforme}')

if __name__ == "__main__":
    main()