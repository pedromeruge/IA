from datetime import datetime

# cada nodo tem um nome e um id

class Node:
    def __init__(self, name, id=-1, start_time="2023-12-01 00:00", end_time="2023-12-01 00:00"):     #  construtor do nodo....."
        self.m_id = id
        self.m_name = str(name)
        self.m_start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        self.m_end_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")

    def __str__(self):
        return "node " + self.m_name

    def setId(self, id):
        self.m_id = id

    def getId(self):
        return self.m_id

    def getName(self):
        return self.m_name
    
    def getStartTime(self):
        return self.m_start_time
    
    def getEndTime(self):
        return self.m_end_time

    def __eq__(self, other):
        return self.m_name == other.m_name

    def __hash__(self):
        return hash(self.m_name)