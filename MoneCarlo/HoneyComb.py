import NumerateHoneycomb
import Link
import Vertex
import Plaquette
import random

class HoneyComb:
    def __init__(self, latticeSize, beta):
        self.__numeratedHoneyComb = NumerateHoneycomb.NumerateHoneycomb(latticeSize)
        self.__linkCount = 3 * (latticeSize * latticeSize)
        self.__vertexCount = 2 * (latticeSize * latticeSize)
        self.__plaquetteCount = latticeSize * latticeSize
        self.__beta = beta
        self.__links = []
        self.__vertices = []
        self.__plaquettes = []
        self.__initiateAll()
        self.__setLinkValues()
        self.__setVertexValues()
        self.__setPlaquetteValue()

    def __initiateAll(self):
        for linkNum in range(self.__linkCount):
            self.__links.append(Link.Link(linkNum))
            self.__links[linkNum].setSpin(random.randint(0, 1))

        for vertexNum in range(self.__vertexCount):
            self.__vertices.append(Vertex.Vertex(vertexNum)) 
        
        for plaquetteNum in range(self.__plaquetteCount):
            self.__plaquettes.append(Plaquette.Plaquette(plaquetteNum))

    def __setLinkValues(self):
        for link in self.__links:
            # finding the corresponding vertices of a link
            for vertexNum in self.__numeratedHoneyComb.linkToVertex[link.getNumber()]:
                link.addVertex(self.__vertices[vertexNum])
            # finding the corresponding plaquettes of a link
            for plaquetteNum in self.__numeratedHoneyComb.linkToPlaquette[link.getNumber()]:
                link.addPlaquette(self.__plaquettes[plaquetteNum])
    
    def __setVertexValues(self):
        for vertex in self.__vertices:
            # finding the corresponding links of a vertex
            for linkNum in self.__numeratedHoneyComb.vertexToLink[vertex.getNumber()]:
                vertex.addLink(self.__links[linkNum])
            # finding the corresponding plaquettes of a vertex
            for plaquetteNum in self.__numeratedHoneyComb.vertexToPlaquette[vertex.getNumber()]:
                vertex.addPlaquette(self.__plaquettes[plaquetteNum])
    
    def __setPlaquetteValue(self):
        for plaquette in self.__plaquettes:
            # finding the corresponding links of a plaquette
            for linkNum in self.__numeratedHoneyComb.plaquetteToLink[plaquette.getNumber()]:
                plaquette.addLink(self.__links[linkNum])
            # finding the corresponding vertices of a plaquette
            for vertexNum in self.__numeratedHoneyComb.plaquetteToVertex[plaquette.getNumber()]:
                plaquette.addVertex(self.__vertices[vertexNum])
    
    def applyStabilizerOperatorA(self, vertex):
        """
            Applies the "A" operator on the given vertex
            ("A" operator applies the sigma x pauli matrix on 
            the adjacent links of a vertex)
        """
        vertex.applyStabilizerOperatorA()

    def applyStabilizerOperatorB(self, plaquetteNum):
        """
            Applies the "B" operator on the given plaquette
            ("B" operator applies the sigma z pauli matrix on 
            the links of a plaquette)
        """
        plaquette = self.__plaquettes[plaquetteNum]
        plaquette.applyStabilizerOperatorB()

    def calculateHamiltoninan(self):
        hamiltonian = 0
        for plaquette in self.__plaquettes:
            if plaquette.hasOddNumberOf1Links():
                hamiltonian += 1
        return hamiltonian
    
    def applyAOnRandomVertex(self):
        vertex = self.__vertices[random.randint(0, self.__vertexCount - 1)]
        vertex.applyStabilizerOperatorA()
        return vertex
