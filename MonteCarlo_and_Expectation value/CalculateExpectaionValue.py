# In the name of God
# SMani24

from typing import List, Tuple
import HoneyComb
import Utils
#TODO: Use the Utils in the main directory

FLOAT_SAVING_FORMAT = '%.40f'

def updateVertexExpectationValue(lattice: HoneyComb.HoneyComb, 
                                 vertexExpectationValue: List[float]) -> None:
    #TODO: add documentation
    tmp = lattice.calculateVertexExpectationValues()
    for i in range(len(vertexExpectationValue)):
        vertexExpectationValue[i] += tmp[i]

def updateLinkExpectationValue(lattice: HoneyComb.HoneyComb, 
                               linkExpectationValue: List[int]) -> None:
    #TODO: add documentation
    tmp = lattice.calculateLinkExpectationValues()
    for i in range(len(linkExpectationValue)):
        linkExpectationValue[i] += tmp[i]

def calculateExpectationValue(statesFilePath, outputFilePath, 
                              latticeSize, beta, lambdaZFilePath, 
                              batchNumber, probabilitySumFilePath):
    """
    For the given batch of states, loops through them and calculates the 
    expectation values based on this batch (for the end result you must loop 
    over all the batches and sum them)
    """
    
    states = Utils.loadCompressedData(statesFilePath)
    print(f"<A> Progress: BatchNumber = {batchNumber} file loaded")
    probabilitySum = float(Utils.loadData(probabilitySumFilePath))
    
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


def multiThreadCalculateExpectationValue(job: Tuple[str, str, int, int, str, int, str]) -> None:
    statesFilePath, outputFilePath, latticeSize, beta, lambdaZFilePath, batchNumber, probabilitySumFilePath = job
    calculateExpectationValue(statesFilePath=statesFilePath, 
                              outputFilePath=outputFilePath,
                              latticeSize=latticeSize, 
                              beta=beta, 
                              lambdaZFilePath=lambdaZFilePath,
                              batchNumber=batchNumber, 
                              probabilitySumFilePath=probabilitySumFilePath)
    