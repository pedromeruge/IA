from datetime import datetime

#package indica localização e prazo de início fim de entrega
class Package:
    def __init__(self, location, weight = 0, volume = 0, start_time="2023-12-01 00:00", end_time="2023-12-01 00:00"):     #  construtor do nodo....."
        self.m_location = location
        self.m_weight = weight
        self.m_volume = volume
        self.m_start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        self.m_end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")

    def __str__(self):

        res = (
            "PACKAGE: location: " + self.m_location + 
            " weight: " + str(self.m_weight) + 
            " volume: " + str(self.m_volume) + 
            " startTime: " + self.m_start_time.strftime("%Y-%m-%d %H:%M:%S") + 
            " endTime: " + self.m_end_time.strftime("%Y-%m-%d %H:%M:%S")
        )
        return res

    def setId(self, id):
        self.m_id = id

    def getId(self):
        return self.m_id

    def getName(self):
        return self.m_name
    
    def getLocation(self):
        return self.m_location
    
    def getWeight(self):
        return self.m_weight
    
    def getVolume(self):
        return self.m_volume
    
    def getStartTime(self):
        return self.m_start_time
    
    def getEndTime(self):
        return self.m_end_time

    def __eq__(self, other):
        return self.m_location == other.m_location

    def __hash__(self):
        return hash(self.m_location)