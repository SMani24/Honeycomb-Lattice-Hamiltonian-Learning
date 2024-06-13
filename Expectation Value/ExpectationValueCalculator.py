


import numpy as np
import ast
import csv
import os

class Numeration:
    def __init__(self, latticeSize):
        self.linkCount = 3 * (latticeSize * latticeSize)
        self.vertexCount = 2 * (latticeSize * latticeSize)
        self.plaquetteCount = latticeSize * latticeSize

        numerationFile = "../MoneCarlo/Numeration/"
        vertexToLinkFilePath = numerationFile + f"LatticeSize={latticeSize}_vertexToLink.csv"
        linkToVertexFilePath = numerationFile + f"LatticeSize={latticeSize}_linkToVertex.csv"
        plaquetteToVertexFilePath = numerationFile + f"LatticeSize={latticeSize}_plaquetteToVertex.csv"
        plaquetteToLinkFilePath = numerationFile + f"LatticeSize={latticeSize}_plaquetteToLink.csv"
        vertexToPlaquetteFilePath = numerationFile + f"LatticeSize={latticeSize}_vertexToPlaquette.csv"
        linkToPlaquetteFilePath = numerationFile + f"LatticeSize={latticeSize}_linkToPlaquette.csv"

        self.vertexToLink = self.__loadFile(vertexToLinkFilePath)
        # print(self.__vertexToLink)
        self.linkToVertex = self.__loadFile(linkToVertexFilePath)
        # print(self.__linkToVertex)
        self.plaquetteToLink = self.__loadFile(plaquetteToLinkFilePath)
        self.plaquetteToVertex = self.__loadFile(plaquetteToVertexFilePath)
        self.vertexToPlaquette = self.__loadFile(vertexToPlaquetteFilePath)
        self.linkToPlaquette = self.__loadFile(linkToPlaquetteFilePath)

    def __loadFile(self, filePath):
        myDict = dict()
        with open(filePath) as csv_file:
            reader = csv.reader(csv_file)
            for key, value in reader:
                key = int(key)
                value = ast.literal_eval(value)
                myDict[key] = value
        return myDict

def loadData(filePath):
    data = np.genfromtxt(filePath, delimiter=',', dtype=str)
    return data

def calculateOccurrences(states):
    occurrences = dict()
    for state in states:
        if not state in occurrences:
            occurrences[state] = 0
        occurrences[state] += 1
    return occurrences

def applySigmaX(linkId, state):
    """
        Applies the sigmaX pauli operator to the given link (and outputs a new state)
    """
    # Finding the char numbers to be changed
    linkPhasePos = 2 * linkId + 1
    linkSpinPos = 2 * linkId
    newSpin = ""
    if state[linkSpinPos] == "1":
        newSpin = "0"
    else:
        newSpin = "1"

    # Calculating the new state:
    newState = state[:linkSpinPos] + newSpin + state[linkSpinPos + 1:]

    return newState


def applyStabilizerOperatorA(vertexId, state, numeration):
    """
        Applies the operator A on the vertex with id "vertexId"
        Note: Can be improved!!!
    """
    linkIds = numeration.vertexToLink[vertexId]
    newState = state
    for linkId in linkIds:
        newState = applySigmaX(linkId, newState)
    # print(state == newState)
    return newState

def calculateAmplitudeProduct(state, newState, numberOfStates, occurrences):
    stateMagnitude = occurrences[state] / numberOfStates
    stateAmplitude = np.sqrt(stateMagnitude)

    if newState in occurrences:
        newStateMagnitude = occurrences[newState] / numberOfStates
        newStateAmplitude = np.sqrt(newStateMagnitude)

        return stateAmplitude * newStateAmplitude
    return 0


def calculateVertex_Ai_ExpectationValue(vertexId, occurrences, numeration, numberOfStates):
    """
        Calculates the <A> for the vertex with id "vertexId"
    """
    answer = 0
    for state in occurrences.keys():
        newState = applyStabilizerOperatorA(vertexId, state, numeration)
        answer += calculateAmplitudeProduct(state, newState, numberOfStates, occurrences)

    print(answer)
    return answer



def calculateVertex_A_ExpectationValue(latticeSize, states, numeration, occurrences):
    """
        given the input file path calculates the <A> for all the vertices
    """
    numberOfStates = len(states)
    
    # for key, value in occurrences.items():
    #     print(value)

    expectationValues = []
    for vertexId in range(numeration.vertexCount):
        expectationValues.append(calculateVertex_Ai_ExpectationValue(vertexId, occurrences, numeration, numberOfStates))
    return expectationValues

def saveData(filePath, data):
    # Making the necessery directories:
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    data = np.array(data)
    np.savetxt(filePath, data, delimiter=',', fmt='%f')

def calculateLink_Ai_ExpectationValue(linkId, occurrences, numeration, numberOfStates):
    answer = 0
    for state in occurrences.keys():
        # Finding the newState:
        vertex1, vertex2 = numeration.linkToVertex[linkId]
        newState = applyStabilizerOperatorA(vertex1, state, numeration)
        newState = applyStabilizerOperatorA(vertex2, newState, numeration)

        answer += calculateAmplitudeProduct(state, newState, numberOfStates, occurrences)
    
    print(answer)
    return answer

def calculateLink_A_ExpectationValue(latticeSize, states, numeration, occurrences):
    """
        Calculates <Ai, Ai + 1> for all the pairs of adjacent vertices (Links)
    """
    numberOfStates = len(states)
    expectationValues = []
    for linkId in range(numeration.linkCount):
        expectationValues.append(calculateLink_Ai_ExpectationValue(linkId, occurrences, numeration, numberOfStates))
    return expectationValues

def run(inputFilePath, outputFilePath, output2FilePath, latticeSize):
    # Loading the states:
    states = loadData(inputFilePath)
    numeration = Numeration(latticeSize)
    occurrences = calculateOccurrences(states)
    # Calculating <A>
    expectationValues = calculateVertex_A_ExpectationValue(latticeSize, states, numeration, occurrences)
    saveData(outputFilePath, expectationValues)

    # Calculating <Ai, Ai+1>:
    expectationValues = calculateLink_A_ExpectationValue(latticeSize, states, numeration, occurrences)
    saveData(output2FilePath, expectationValues)
run("./configNumber=3.csv", "./out.csv", "./out2.csv", 8)