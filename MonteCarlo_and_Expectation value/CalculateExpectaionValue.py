# In the name of God
# SMani24

import HoneyComb
import Utils

FLOAT_SAVING_FORMAT = '%.20f'

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
    print(f"<A> Progress: BatchNumber = {batchNumber} file loaded")
    probabilitySum = float(states[0])
    
    # Initiating the lattice
    lattice = HoneyComb.HoneyComb(latticeSize=latticeSize, beta=beta, lambdaZFilePath=lambdaZFilePath)
    lattice.setAmplitudeDenominator(probabilitySum ** 0.5)

    # Initiating the expectation value arrays
    vertexExpectationValues = [0] * lattice.getVertexCount()
    linkExpectationValues = [0] * lattice.getLinkCount()

    for stateNumber, state in enumerate(states):
        if stateNumber == 0:
            continue
        lattice.loadState(state)
        
        updateVertexExpectationValue(lattice, vertexExpectationValues)
        # updateLinkExpectationValue(lattice, linkExpectationValues)

        if stateNumber % 1000 == 0:
            print(f"<A> Progress: BatchNumber = {batchNumber} {int(stateNumber / len(states) * 100)}%")
    
    vertexExpectationValuesFilePath = outputFilePath + "vertexExpectationValues.csv"
    linkExpectationValuesFilePath = outputFilePath + "linkExpectationValues.csv"

    Utils.saveData(vertexExpectationValuesFilePath, vertexExpectationValues, FLOAT_SAVING_FORMAT)
    # Utils.saveData(linkExpectationValuesFilePath, linkExpectationValues, FLOAT_SAVING_FORMAT)
    print(f"<A> Progress: BatchNumber = {batchNumber} expectation values saved succesfuly")
    
    del lattice
    del states
    del linkExpectationValues
    del vertexExpectationValues


def multiThreadCalculateExpectationValue(job):
    statesFilePath, outputFilePath, latticeSize, beta, lambdaZFilePath, batchNumber = job
    calculateExpectationValue(statesFilePath=statesFilePath, outputFilePath=outputFilePath,
                              latticeSize=latticeSize, beta=beta, lambdaZFilePath=lambdaZFilePath,
                              batchNumber=batchNumber)
    