# In the name of God
# SMani24

class Link:
    def __init__(self, number, beta, lambdaZ):
        self.__spin = 0 # the state of the link, either |0> or |1>
        self.__phase = 1 # either 1 or -1
        self.__number = number
        self.__beta = beta
        self.__lambdaZ = lambdaZ
        self.__lambdaX = 0
        self.__vertices = []
        self.__plaquettes = []
    
    def setVertices(self, vertices):
        self.__vertices = vertices

    def setSpin(self, spin):
        self.__spin = spin

    def setPhase(self, phase):
        self.__phase = phase

    def getVertices(self):
        return self.__vertices
    
    def getPlaquettes(self):
        return self.__plaquettes
    
    def getNumber(self):
        return self.__number
    
    def getSpin(self):
        return self.__spin
    
    def getPhase(self):
        return self.__phase
    
    def getBeta(self):
        return self.__beta

    def getLambdaZ(self):
        return self.__lambdaZ
    
    def getAdjacentLinks(self):
        """
        returns a list of adjacent links to this link (including itself)
        """
        adjacentLinks = []
        for vertex in self.__vertices:
            adjacentLinks += vertex.getLinks()
        return list(set(adjacentLinks)) # to remove duplicates in the links
    
    def addVertex(self, vertex):
        self.__vertices.append(vertex)

    def addPlaquette(self, plaquette):
        self.__plaquettes.append(plaquette)
    
    def applySigmaX(self):
        self.__spin = 1 - self.__spin

    def applySigmaZ(self):
        if self.__spin == 1:
            self.__phase *= -1

    def hasLambdaZError(self):
        if self.__lambdaZ != 0:
            return True
        return False

    