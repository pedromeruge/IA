from datetime import datetime

#package indica localização e prazo de início fim de entrega
class Package:
    def __init__(self, location, start_time="2023-12-01 00:00", end_time="2023-12-01 00:00"):     #  construtor do nodo....."
        self.m_location = location
        self.m_start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        self.m_end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")

    def __str__(self):
        return "package for " + self.m_location

    def setId(self, id):
        self.m_id = id

    def getId(self):
        return self.m_id

    def getName(self):
        return self.m_name
    
    def getLocation(self):
        return self.m_location
    
    def getStartTime(self):
        return self.m_start_time
    
    def getEndTime(self):
        return self.m_end_time

    def __eq__(self, other):
        return self.m_location == other.m_location

    def __hash__(self):
        return hash(self.m_location)