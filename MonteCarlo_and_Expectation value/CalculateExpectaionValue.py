# In the name of God
# SMani24

import HoneyComb
import Utils

def updateVertexExpectationValue(lattice, vertexExpectationValue):
    # print(lattice.calculateVertexExpectationValues())
    tmp = lattice.calculateVertexExpectationValues()
    # print(max(tmp))
    for i in range(len(vertexExpectationValue)):
        vertexExpectationValue[i] += tmp[i]

def updateLinkExpectationValue(lattice, linkExpectationValue):
    # print(lattice.calculateLinkExpectationValues())
    tmp = lattice.calculateLinkExpectationValues()
    # print(max(tmp))
    for i in range(len(linkExpectationValue)):
        linkExpectationValue[i] += tmp[i]

def calculateExpectationValue(statesFilePath, outputFilePath, latticeSize, beta, lambdaZFilePath, batchNumber):
    """
    For the given batch of states, loops through them and calculates the 
    expectation values based on this batch (for the end result you must loop 
    over all the batches and sum them)
    """
    
    states = Utils.loadData(statesFilePath)
    probabilitySum = float(states[0])
    
    # Initiating the lattice
    lattice = HoneyComb.HoneyComb(latticeSize=latticeSize, beta=beta, lambdaZFilePath=lambdaZFilePath)
    lattice.setAmplitudeDenominator(probabilitySum ** 0.5)

    # Initiating the expectation value arrays
    vertexExpectationValues = [0] * lattice.getVertexCount()
    linkExpectationValues = [0] * lattice.getLinkCount()

    for stateNumber, state in enumerate(states):
        if stateNumber == 1:
            continue
        lattice.loadState(state)
        
        updateVertexExpectationValue(lattice, vertexExpectationValues)
        updateLinkExpectationValue(lattice, linkExpectationValues)

        if stateNumber % 1000 == 0:
            print(f"<A> Progress: BatchNumber = {batchNumber} {int(stateNumber / len(states) * 100)}%")
    
    Utils.saveData(outputFilePath, [vertexExpectationValues, linkExpectationValues])
    
    del lattice
    del states
    del linkExpectationValues
    del vertexExpectationValues


def multiThreadCalculateExpectationValue(job):
    statesFilePath, outputFilePath, latticeSize, beta, lambdaZFilePath, batchNumber = job
    calculateExpectationValue(statesFilePath=statesFilePath, outputFilePath=outputFilePath,
                              latticeSize=latticeSize, beta=beta, lambdaZFilePath=lambdaZFilePath,
                              batchNumber=batchNumber)
    