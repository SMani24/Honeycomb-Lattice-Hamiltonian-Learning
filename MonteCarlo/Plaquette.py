class Plaquette:
    def __init__(self, number):
        self.__number = number
        self.__vertices = []
        self.__links = []

    def getNumber(self):
        return self.__number
    
    def addVertex(self, vertex):
        self.__vertices.append(vertex)
    
    def addLink(self, link):
        self.__links.append(link)

    def applyStabilizerOperatorB(self):
        for link in self.__links:
            link.applySigmaZ()
    
    def calculateNumberOf1Links(self):
        numberOf1Links = 0
        for link in self.__links:
            if link.getSpin() == 1:
                numberOf1Links += 1
        return numberOf1Links
    