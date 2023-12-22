from datetime import datetime

# cada nodo tem um nome e um id

class Node:
    def __init__(self, name, id=-1):     #  construtor do nodo....."
        self.m_id = id
        self.m_location = str(name)

    def __str__(self):
        return "node " + self.m_location

    def setId(self, id):
        self.m_id = id

    def getId(self):
        return self.m_id

    def getName(self):
        return self.m_location
    
    def __eq__(self, other):
        return self.m_location == other.m_location

    def __hash__(self):
        return hash(self.m_name)
    
    def __str__(self):
        return "Node: " + str(self.m_id) + " Location: " + self.m_location