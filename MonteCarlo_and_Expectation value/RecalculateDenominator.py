# In the name of God
# SMani24


import Utils
import HoneyComb
from typing import List, Tuple

FLOAT_SAVING_FORMAT = '%.40f'

def UniteFiles(tmpOutputFilePaths: List[str], statesFilePaths: List[str]) -> None:
    probabilitySum = 0
    for tmpOutputFilePath in tmpOutputFilePaths:
        partialProbabilitySum = float(Utils.loadData(filePath=tmpOutputFilePath))
        probabilitySum += partialProbabilitySum

    for cnt, statesFilePath in enumerate(statesFilePaths):
        states = Utils.loadData(filePath=statesFilePath)
        # print(states[0])
        states[0] = f"{probabilitySum:.40f}"
        Utils.saveData(filePath=statesFilePath, data=states)
        print(f"{cnt} batches done!")

def RecalculateDenominator(statesFilePath: str, latticeSize: int, 
                           beta: int, lambdaZFilePath: str,
                           batchNumber: int, tmpOutPutDir: str) -> None:
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
    print(f"Recalculation of Denominator: BatchNumber = {batchNumber} finished!")

def multiThreadRecalculateDenominator(job: Tuple[str, int, int, str, int, str]) -> None:
    statesFilePath, latticeSize, beta, lambdaZFilePath, batchNumber, tmpOutputFilePath = job
    RecalculateDenominator(statesFilePath=statesFilePath, 
                           latticeSize=latticeSize,
                           beta=beta, lambdaZFilePath=lambdaZFilePath,
                           batchNumber=batchNumber, tmpOutPutDir=tmpOutputFilePath)
    