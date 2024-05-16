import math

class Vertex:
    def __init__(self, number):
        self.__number = number
        self.__links = []
        self.__plaquettes = []

    def getNumber(self):
        return self.__number
    
    def getLinks(self):
        return self.__links
    
    def addLink(self, link):
        self.__links.append(link)

    def addPlaquette(self, plaquette):
        self.__plaquettes.append(plaquette)
    
    def applyStabilizerOperatorA(self):
        for link in self.__links:
            link.applySigmaX()

    def calculateLinkPhaseProduct(self):
        phaseProduct = 1
        for link in self.__links:
            phaseProduct *= link.getPhase()
        return phaseProduct

    def calculateError(self):
        """
        returns the following: 
            exp{beta * sigma{lambda * Z} over all the links of the vertex}
            where Z is the pauli operator Z
        """
        result = 0
        for link in self.__links:
            link.applySigmaZ()
            result += (-1) * link.getBeta() * link.getLambdaZ() * link.getPhase()
            link.applySigmaZ()
        return math.exp(result)
         