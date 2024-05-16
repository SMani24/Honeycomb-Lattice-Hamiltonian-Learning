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
    
    def addVertex(self, vertex):
        self.__vertices.append(vertex)

    def addPlaquette(self, plaquette):
        self.__plaquettes.append(plaquette)
    
    def applySigmaX(self):
        self.__spin = 1 - self.__spin

    def applySigmaZ(self):
        if self.__spin == 1:
            self.__phase *= -1

    