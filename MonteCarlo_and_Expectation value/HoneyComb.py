# In the name of God
# SMani24
# Ali Kookani

import ast
import Link
import Vertex
import Plaquette
import random
import numpy as np
import math
import csv

class HoneyComb:
    def __init__(self, latticeSize, beta, lambdaZFilePath=""):
        self.__loadNumeration(latticeSize)
        self.__linkCount = 3 * (latticeSize * latticeSize)
        self.__vertexCount = 2 * (latticeSize * latticeSize)
        self.__plaquetteCount = latticeSize * latticeSize
        self.__beta = beta
        self.__links = []
        self.__vertices = []
        self.__plaquettes = []
        self.__initiateAll(lambdaZFilePath)
        self.__setLinkValues()
        self.__setVertexValues()
        self.__setPlaquetteValue()
        self.__deleteNumertaion()
        self.energy = self.__calculateWholeLatticeEnergy()
        self.__amplitude = self.__calculateAmplitude()
        self.__amplitudeDenominator = 1

    def __deleteNumertaion(self):
        del self.__vertexToLink
        del self.__linkToVertex
        del self.__plaquetteToLink
        del self.__plaquetteToVertex
        del self.__vertexToPlaquette
        del self.__linkToPlaquette

    def __loadFile(self, filePath):
        myDict = dict()
        with open(filePath) as csv_file:
            reader = csv.reader(csv_file)
            for key, value in reader:
                key = int(key)
                value = ast.literal_eval(value)
                myDict[key] = value
        return myDict

    def __loadNumeration(self, latticeSize):
        numerationFile = "./Numeration/"
        vertexToLinkFilePath = numerationFile + f"LatticeSize={latticeSize}_vertexToLink.csv"
        linkToVertexFilePath = numerationFile + f"LatticeSize={latticeSize}_linkToVertex.csv"
        plaquetteToLinkFilePath = numerationFile + f"LatticeSize={latticeSize}_plaquetteToLink.csv"
        plaquetteToVertexFilePath = numerationFile + f"LatticeSize={latticeSize}_plaquetteToVertex.csv"
        vertexToPlaquetteFilePath = numerationFile + f"LatticeSize={latticeSize}_vertexToPlaquette.csv"
        linkToPlaquetteFilePath = numerationFile + f"LatticeSize={latticeSize}_linkToPlaquette.csv"
        
        self.__vertexToLink = self.__loadFile(vertexToLinkFilePath)
        # print(self.__vertexToLink)
        self.__linkToVertex = self.__loadFile(linkToVertexFilePath)
        # print(self.__linkToVertex)
        self.__plaquetteToLink = self.__loadFile(plaquetteToLinkFilePath)
        self.__plaquetteToVertex = self.__loadFile(plaquetteToVertexFilePath)
        self.__vertexToPlaquette = self.__loadFile(vertexToPlaquetteFilePath)
        self.__linkToPlaquette = self.__loadFile(linkToPlaquetteFilePath)

    def __initiateAll(self, lambdaZFilePath):
        lambdaZConfig = np.zeros(self.__linkCount) # This is an array where i th value corresponds to the lambdaZ of i th link
        if lambdaZFilePath != "":
            lambdaZConfig = np.loadtxt(lambdaZFilePath, delimiter=',')
        for linkNum in range(self.__linkCount):
            self.__links.append(Link.Link(linkNum, self.__beta, lambdaZConfig[linkNum]))
            # self.__links[linkNum].setSpin(random.randint(0, 1))

        for vertexNum in range(self.__vertexCount):
            self.__vertices.append(Vertex.Vertex(vertexNum)) 
        
        for plaquetteNum in range(self.__plaquetteCount):
            self.__plaquettes.append(Plaquette.Plaquette(plaquetteNum))

    def __setLinkValues(self):
        for link in self.__links:
            # finding the corresponding vertices of a link
            for vertexNum in self.__linkToVertex[link.getNumber()]:
                link.addVertex(self.__vertices[vertexNum])
            # finding the corresponding plaquettes of a link
            for plaquetteNum in self.__linkToPlaquette[link.getNumber()]:
                link.addPlaquette(self.__plaquettes[plaquetteNum])
    
    def __setVertexValues(self):
        for vertex in self.__vertices:
            # finding the corresponding links of a vertex
            for linkNum in self.__vertexToLink[vertex.getNumber()]:
                vertex.addLink(self.__links[linkNum])
            # finding the corresponding plaquettes of a vertex
            for plaquetteNum in self.__vertexToPlaquette[vertex.getNumber()]:
                vertex.addPlaquette(self.__plaquettes[plaquetteNum])
    
    def __setPlaquetteValue(self):
        for plaquette in self.__plaquettes:
            # finding the corresponding links of a plaquette
            for linkNum in self.__plaquetteToLink[plaquette.getNumber()]:
                plaquette.addLink(self.__links[linkNum])
            # finding the corresponding vertices of a plaquette
            for vertexNum in self.__plaquetteToVertex[plaquette.getNumber()]:
                plaquette.addVertex(self.__vertices[vertexNum])      

    def __calculatePartialAmplitude(self, links):
        """
            only calculates the Amplitude for the given links
            (instead of looping over all the links)
        """
        power = 0
        for link in links:
            link.applySigmaZ()
            power += link.getLambdaZ() * link.getPhase()
            link.applySigmaZ()
        power *= (self.__beta / 2)
        return math.exp(power)

    def __calculateAmplitude(self):
        """
            Loops over all the links and calculates the Amplitude of 
            the current state
        """
        return self.__calculatePartialAmplitude(self.__links)
    
    def __updateAmplitude(self, oldAmplitude, newAmplitude):
        self.__amplitude *= newAmplitude / oldAmplitude
    
    # getters:
    def getLinkCount(self):
        return self.__linkCount
    
    def getVertexCount(self):
        return self.__vertexCount
    
    def getPlaquetteCount(self):
        return self.__plaquetteCount
    
    def getLinkByNumber(self, linkNumber):
        return self.__links[linkNumber]
    
    def getProbability(self):
        return (self.__amplitude / self.__amplitudeDenominator) ** 2

    def applyStabilizerOperatorA(self, vertices):
        """
            Applies the "A" operator on the given vertex
            and updates the lattice's energy
            ("A" operator applies the sigma x pauli matrix on 
            the adjacent links of a vertex)
        """
        # Making sure the input is a list of vertices rather than a single vertex:
        if type(vertices) != type([]):
            vertices = [vertices]

        for vertex in vertices:
            changedLinks = vertex.getLinks()
            # the value that needs to be removed from the Amplitude
            removedAmplitude = self.__calculatePartialAmplitude(changedLinks)

            oldEnergy = self.__calculateEnergy(changedLinks)
            vertex.applyStabilizerOperatorA()
            newEnergy = self.__calculateEnergy(changedLinks)
            # the value that needs to be added to the Amplitude
            addedAmplitude = self.__calculatePartialAmplitude(changedLinks)
            
            self.__updateAmplitude(removedAmplitude, addedAmplitude)
            self.energy += newEnergy - oldEnergy

    def applyStabilizerOperatorB(self, plaquetteNum):
        """
            Needs to be fixed!!
            Applies the "B" operator on the given plaquette
            ("B" operator applies the sigma z pauli matrix on 
            the links of a plaquette)
        """
        plaquette = self.__plaquettes[plaquetteNum]
        plaquette.applyStabilizerOperatorB()

    def __calculateVertexEnergy(self, vertex):
        energy = 0
        # Calculating <A>: <A> is zero
        energy += 0
        # Calculating the exp term:
        energy += vertex.calculateError()
        return energy

    def __calculatePlaquetteEnergy(self, plaquette):
        energy = 0
        # Calculating <B>
        energy += (-1) * ((-1) ^ (plaquette.calculateNumberOf1Links()))
        return energy

    def __calculateWholeLatticeEnergy(self):
        energy = 0
        for vertex in self.__vertices:
            energy += self.__calculateVertexEnergy(vertex)

        for plaquette in self.__plaquettes:
            energy += self.__calculatePlaquetteEnergy(plaquette)
        return energy


    def __calculateEnergy(self, links):
        # Finding the adjacent vertices of the given links:
        vertices = set()
        for link in links:
            for vertex in link.getVertices():
                vertices.add(vertex)

        # Finding the adjacent palquettes of the given links:
        plaquettes = set()
        for link in links:
            for plaquette in link.getPlaquettes():
                plaquettes.add(plaquette)

        energy = 0
        for vertex in vertices:
            energy += self.__calculateVertexEnergy(vertex)

        # for plaquette in plaquettes:
        #     energy += self.__calculatePlaquetteEnergy(plaquette)
        
        return energy
    
    def selectRandomVertex(self):
        return self.__vertices[random.randint(0, self.__vertexCount - 1)]
    
    def selectRandomLink(self):
        return self.__links[random.randint(0, self.__linkCount - 1)]
    
    def __calculateExpectationValue(self, vertices):
        """
            for the given vertices and the current state of the lattice
            applies the stabilizer operator A on them to find their 
            corresponding couple state, then multiplies the two states 
            amplitudes to calculate <A> for this particular state and vertex
        """
        oldAmplitude = self.__amplitude
        self.applyStabilizerOperatorA(vertices)
        newAmplitude = self.__amplitude
        # reversing the changes to the state:
        self.applyStabilizerOperatorA(vertices)
        return oldAmplitude * newAmplitude / (self.__amplitudeDenominator ** 2)

    def calculateVertexExpectationValues(self):
        """
            Loops over all the vertices and calculates <A> for them and 
            returns a numpy array with the size of the vertices where the i th 
            number corresponds to <A> for the i th vertex
        """
        vertexExpectationValues = [0] * self.__vertexCount
        for vertex in self.__vertices:
            vertexExpectationValues[vertex.getNumber()] = self.__calculateExpectationValue(vertex)
        return vertexExpectationValues
    
    def calculateLinkExpectationValues(self):
        """
            Loops over all the links and calculates <A> for them and returns
            a numpy array with the size of the links where the i th 
            number corresponds to <A> for the i th link
        """
        linkExpectationValues = np.zeros(self.__linkCount)
        for link in self.__links:
            vertices = link.getVertices()
            linkExpectationValues[link.getNumber()] = self.__calculateExpectationValue(vertices)
        return linkExpectationValues

    def printLinks(self):
        linkStr = ""
        for link in self.__links:
            linkStr += str(link.getSpin())
        print(linkStr)
    
    def generateStateString(self):
        """
        It will output a string of the state. 
        Character 2k represents the spin of the link number k (0 for |0> and 1 for |1>)
        and character 2k + 1 represents the phase of the link number k (0 for -1 and 1 for 1)
        """
        stateString = ""
        for linkNumber in range(self.__linkCount):
            link = self.getLinkByNumber(linkNumber)
            # adding the spin:
            if link.getSpin() == 0:
                stateString += '0'
            if link.getSpin() == 1:
                stateString += '1'
            # adding the phase:
            if link.getPhase() == 1:
                stateString += '1'
            if link.getPhase() == -1:
                stateString += '0'
        return stateString
    
    def loadState(self, state):
        """
            Loads the given state to the lattice
            (sets the values of spins and phase of every link)
        """
        for i, char in enumerate(state):
            linkNumber = int(i / 2)
            link = self.getLinkByNumber(linkNumber)
            if i % 2 == 0:
                if char == '0':
                    link.setSpin(0)
                if char == '1':
                    link.setSpin(1)
            
            else:
                if char == '0':
                    link.setPhase(-1)
                if char == '1':
                    link.setPhase(1)

    def setAmplitudeDenominator(self, denominator):
        self.__amplitudeDenominator = denominator
    
    def generateVertexLambdaZErrorList(self):
        """
            Generates a list of 0s and 1s, ith index is 0 when the ith vertex
            has no links with error and 1 otherwise
        """
        errorList = []
        for vertex in self.__vertices:
            if vertex.hasLambdaZError():
                errorList.append((vertex.getNumber(), 1))
            else:
                errorList.append((vertex.getNumber(), 0))
        return errorList
