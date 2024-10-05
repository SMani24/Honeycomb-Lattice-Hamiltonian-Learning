# In the name of God
# SMani24

import multiprocessing as mp
import numpy as np
import Utils
import CalculateExpectaionValue
import CalculateVertexFlipProbability
import time
import MonteCarlo
import os

startTime = time.time()

NUMBER_OF_ITERATIONS = int(1e4)
NUMBER_OF_SAMPLES = int(1e3)

FLOAT_SAVING_FORMAT = '%.20f'

LATTICE_SIZES = [8]
BETAS = [0.5]
SINGLE_QUBIT_ERROR_PROBABILITES = [0.0, 0.05, 0.1, 0.15, 0.2]
CONFIG_NUMBER_RANGE = range(1)
BATCH_RANGE = range(3000)

def sumExpectationValues():
    for latticeSize in LATTICE_SIZES:
        linkCount = 3 * (latticeSize * latticeSize)
        vertexCount = 2 * (latticeSize * latticeSize)
        for beta in BETAS:
            for singleQubitErrorProbability in SINGLE_QUBIT_ERROR_PROBABILITES:
                for configNumber in CONFIG_NUMBER_RANGE:
                    vertexExpectationValues = np.zeros(vertexCount)
                    linkExpectationValues = np.zeros(linkCount)
                    for batchNumber in BATCH_RANGE:
                        outputFilePath = f"./ExpectationValues/PartialExpectationValue/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/configNumber={configNumber}/Batch={batchNumber}_"
                        vertexExpectationValuesFilePath = outputFilePath + "vertexExpectationValues.csv"
                        linkExpectationValuesFilePath = outputFilePath + "linkExpectationValues.csv"
                        
                        if os.path.isfile(vertexExpectationValuesFilePath) == False or os.path.isfile(linkExpectationValuesFilePath) == False:
                                continue
                        
                        batchVertexExpectationValue = Utils.loadData(vertexExpectationValuesFilePath, float)
                        batchLinkExpectationValue = Utils.loadData(linkExpectationValuesFilePath, float)

                        vertexExpectationValues += batchVertexExpectationValue
                        linkExpectationValues += batchLinkExpectationValue

                    outputFilePath = f"./ExpectationValues/FinalExpectationValue/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/"
                    vertexExpectationValuesFilePath = outputFilePath + f"vertex_A_ExpectationValue_configNumber={configNumber}.csv"
                    linkExpectationValuesFilePath = outputFilePath + f"link_A_ExpectationValue_configNumber={configNumber}.csv"
                    Utils.saveData(vertexExpectationValuesFilePath, vertexExpectationValues, FLOAT_SAVING_FORMAT)
                    Utils.saveData(linkExpectationValuesFilePath, linkExpectationValues, FLOAT_SAVING_FORMAT)


if __name__ == "__main__":
    threadNumber = int(input("Enter the number of threades to be used: "))
    codeToRun = input("""
--- MC to run MonteCarlo
--- A to calculate <A>
--- S to sum all partial <A>
--- P to draw the plot:  """)

    mp.freeze_support()
    pool = mp.Pool(threadNumber)
    
    poolJobs = []

    if codeToRun.upper() == "S":
        sumExpectationValues()
        print("Done!")
    
    if codeToRun.upper() == "P":
        CalculateVertexFlipProbability.drawPlot(BETA=BETAS, LATTICE_SIZE=LATTICE_SIZES, CONFIG_RANGE=CONFIG_NUMBER_RANGE,
                                                SINGLE_QUBIT_ERROR_PROBABILITIES=SINGLE_QUBIT_ERROR_PROBABILITES)

    if codeToRun.upper() == "MC":

        for latticeSize in LATTICE_SIZES:
            for beta in BETAS:
                for singleQubitErrorProbability in SINGLE_QUBIT_ERROR_PROBABILITES:
                    for configNumber in CONFIG_NUMBER_RANGE:
                        lambdaZFilePath = f"./LambdaConfigs/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/VertexLmabdaConfig={configNumber}.csv"
                        poolJobs.append((latticeSize, beta, lambdaZFilePath, singleQubitErrorProbability, NUMBER_OF_ITERATIONS, NUMBER_OF_SAMPLES, configNumber))

        pool.map(MonteCarlo.multithreadMonteCarlo, poolJobs)
        finishTime = time.time()
        print("Total time: ", finishTime - startTime)
    
    elif codeToRun.upper() == 'A':

        for latticeSize in LATTICE_SIZES:
            for beta in BETAS:
                for singleQubitErrorProbability in SINGLE_QUBIT_ERROR_PROBABILITES:
                    for configNumber in CONFIG_NUMBER_RANGE:
                        lambdaZFilePath = f"./LambdaConfigs/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/VertexLmabdaConfig={configNumber}.csv"
                        for batchNumber in BATCH_RANGE:
                            statesFilePath = f"./MCOutput/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/configNumber={configNumber}/Batch={batchNumber}.csv"
                            outputFilePath = f"./ExpectationValues/PartialExpectationValue/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/configNumber={configNumber}/Batch={batchNumber}_"
                            vertexExpectationValuesFilePath = outputFilePath + "vertexExpectationValues.csv"
                            linkExpectationValuesFilePath = outputFilePath + "linkExpectationValues.csv"
                            
                            if os.path.isfile(statesFilePath) == False or (os.path.isfile(vertexExpectationValuesFilePath ) == True and os.path.isfile(linkExpectationValuesFilePath) == True):
                                continue
                            poolJobs.append((statesFilePath, outputFilePath, latticeSize, beta, lambdaZFilePath, batchNumber))
        
        pool.map(CalculateExpectaionValue.multiThreadCalculateExpectationValue, poolJobs)
        finishTime = time.time()
        print("Total time: ", finishTime - startTime)