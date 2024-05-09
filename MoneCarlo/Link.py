class Link:
    def __init__(self, number):
        self.__spin = 0 # the state of the link, either |0> or |1>
        self.__phase = 1 # either 1 or -1
        self.__number = number
        self.__phaseLambda = 0
        self.__spinLambda = 0
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
    
    def addVertex(self, vertex):
        self.__vertices.append(vertex)

    def addPlaquette(self, plaquette):
        self.__plaquettes.append(plaquette)
    
    def applySigmaX(self):
        self.__spin = 1 -self.__spin

    def applySigmaZ(self):
        self.__phase *= -1

    