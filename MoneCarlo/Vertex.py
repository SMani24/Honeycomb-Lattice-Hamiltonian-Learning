class Vertex:
    def __init__(self, number):
        self.__number = number
        self.__links = []
        self.__plaquettes = []

    def getNumber(self):
        return self.__number
    
    def addLink(self, link):
        self.__links.append(link)

    def addPlaquette(self, plaquette):
        self.__plaquettes.append(plaquette)
    
    def applyStabilizerOperatorA(self):
        for link in self.__links:
            link.applySigmaX()