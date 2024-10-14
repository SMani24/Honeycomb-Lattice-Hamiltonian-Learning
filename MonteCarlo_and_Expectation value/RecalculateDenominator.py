# In the name of God
# SMani24

import HoneyComb
import Utils

FLOAT_SAVING_FORMAT = '%.40f'

def UniteFiles(tmpOutputFilePaths: list[str], statesFilePaths: list[str]): #TODO: ask Moein how to distinguish voids
    probabilitySum = 0
    for tmpOutputFilePath in tmpOutputFilePaths:
        partialProbabilitySum = Utils.loadData(filePath=tmpOutputFilePath, dtype=FLOAT_SAVING_FORMAT)
        probabilitySum += partialProbabilitySum
    
    for statesFilePath in statesFilePaths:
        states = Utils.loadData(filePath=statesFilePath)
        states[0] = f"{probabilitySum:.40f}"

        Utils.saveData(filePath=statesFilePath, data=states)

def RecalculateDenominator(statesFilePath: str, latticeSize: int, 
                           beta: int, lambdaZFilePath: str,
                           batchNumber: int, tmpOutPutDir: str): #TODO: ask Moein how to distinguish voids
    """
        Recalculates the denominator stored in the up batch file in case
        of an error. Note that it only partially calculates the denominator
        based on the states in a single file, the results need to be summed 
        over to get the final denominator
    """
    # Loading the states
    states = Utils.loadData(statesFilePath)
    print(f"Recalculation of Denominator: BatchNumber = {batchNumber} file loaded")
    
    # Initializing lattice
    lattice = HoneyComb.HoneyComb(latticeSize=latticeSize, beta=beta,
                                  lambdaZFilePath=lambdaZFilePath)

    partialProbabilitySum = 0
    for stateNumber, state in enumerate(states):
        if stateNumber == 0:
            continue
        lattice.loadState(state)
        partialProbabilitySum += lattice.getProbability()

    Utils.saveData(tmpOutPutDir, partialProbabilitySum, format=FLOAT_SAVING_FORMAT)

def multiThreadRecalculateDenominator(job):
    statesFilePath, latticeSize, beta, lambdaZFilePath, batchNumber, tmpOutputFilePath = job
    RecalculateDenominator(statesFilePath=statesFilePath, 
                           latticeSize=latticeSize,
                           beta=beta, lambdaZFilePath=lambdaZFilePath,
                           batchNumber=batchNumber, tmpOutPutDir=tmpOutputFilePath)
    