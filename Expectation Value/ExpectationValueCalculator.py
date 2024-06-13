


import numpy as np
import Utils

def calculateAmplitudeProduct(state, newState, numberOfStates, occurrences):
    """
        Calculates the amplitudes of the given two states and returns their product
        if the newState isn't in the occurrences the function will return 0
    """
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
        newState = Utils.applyStabilizerOperatorA(vertexId, state, numeration)
        answer += calculateAmplitudeProduct(state, newState, numberOfStates, occurrences)
    return answer

def calculateVertex_A_ExpectationValue(states, numeration, occurrences):
    """
        given the input file path calculates the <A> for all the vertices
    """
    numberOfStates = len(states)

    expectationValues = []
    for vertexId in range(numeration.vertexCount):
        expectationValues.append(calculateVertex_Ai_ExpectationValue(vertexId, occurrences, numeration, numberOfStates))
    return expectationValues

def calculateLink_Ai_ExpectationValue(linkId, occurrences, numeration, numberOfStates):
    answer = 0
    for state in occurrences.keys():
        # Finding the newState:
        vertex1, vertex2 = numeration.linkToVertex[linkId]
        newState = Utils.applyStabilizerOperatorA(vertex1, state, numeration)
        newState = Utils.applyStabilizerOperatorA(vertex2, newState, numeration)

        answer += calculateAmplitudeProduct(state, newState, numberOfStates, occurrences)

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

def run(inputFilePath, vertex_A_ExpectationValueFilePath, link_A_ExpectationValueFilePath, latticeSize):
    # Loading the states:
    states = Utils.loadData(inputFilePath)
    numeration = Utils.Numeration(latticeSize)
    occurrences = Utils.calculateOccurrences(states)
    print(f"Occurrences calculated")
    # Calculating <A>
    expectationValues = calculateVertex_A_ExpectationValue(states, numeration, occurrences)
    Utils.saveData(vertex_A_ExpectationValueFilePath, expectationValues)
    print("<A> saved!")
    # Calculating <Ai, Ai+1>:
    expectationValues = calculateLink_A_ExpectationValue(latticeSize, states, numeration, occurrences)
    Utils.saveData(link_A_ExpectationValueFilePath, expectationValues)
    print("<Ai, Ai+1> saved!")

def multithreadRun(job):
    inputFilePath, vertex_A_ExpectationValueFilePath, link_A_ExpectationValueFilePath, latticeSize = job
    run(inputFilePath, vertex_A_ExpectationValueFilePath, link_A_ExpectationValueFilePath, latticeSize)