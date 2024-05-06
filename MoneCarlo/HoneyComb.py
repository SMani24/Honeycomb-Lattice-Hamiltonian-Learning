import NumerateHoneycomb
import Link
import Vertex
import Plaquette

class HoneyComb:
    def __init__(self, latticeSize):
        self.numeratedHoneyComb = NumerateHoneycomb(latticeSize)
        self.__linkCount = 3 * (latticeSize * latticeSize)
        self.__vertexCount = 2 * (latticeSize * latticeSize)
        self.__plaquetteCount = latticeSize * latticeSize
        self.__links = []
        self.__vertices = []
        self.__plaquettes = []
        self.__initiateLinks()
        self.__initiateVertices()


    def __initiateLinks(self):
        for linkNum in range(self.__linkCount):
            self.__links.append(Link.Link(linkNum))
    
    def __initiateVertices(self):
        for vertexNum in range(self.__vertexCount):
            links = []
            for linkNum in self.numeratedHoneyComb.vertexToLink[vertexNum]:
                links.append(self.__links[linkNum])
            self.__vertices.append(Vertex.Vertex(vertexNum, links))
    
    def __initiatePlaquettes(self):
        for plaquetteNum in range(self.__plaquetteCount):
            vertices = []
            for vertexNum in self.numeratedHoneyComb.plaquetteToVertex[plaquetteNum]:
                vertices.append(self.__vertices[vertexNum])
            links = []
            for linkNum in self.numeratedHoneyComb.plaquetteToLink[plaquetteNum]:
                links.append(self.__links[linkNum])
            self.plaquettes.append(Plaquette.Plaquette(number, vertices, links))