# In the name of God
# SMani24
# Ali Kookani
import multiprocessing as mp
import CalculateExpectaionValue
import time
import MonteCarlo
import os

startTime = time.time()

NUMBER_OF_ITERATIONS = int(1e4)
NUMBER_OF_SAMPLES = int(1e3)

LATTICE_SIZES = [8]
BETAS = [0.5]
SINGLE_QUBIT_ERROR_PROBABILITES = [0.0, 0.05, 0.1, 0.15, 0.2]
CONFIG_NUMBER_RANGE = range(1)
BATCH_RANGE = range(125)

if __name__ == "__main__":
    threadNumber = int(input("Enter the number of threades to be used: "))
    codeToRun = input("Enter MC to run MonteCarlo or enter A to calculate <A>: ")

    mp.freeze_support()
    pool = mp.Pool(threadNumber)
    
    poolJobs = []

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
                            outputFilePath = f"./ExpectationValues/PartialExpectationValue/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/configNumber={configNumber}/Batch={batchNumber}.csv"
                            if os.path.isfile(statesFilePath) == False:
                                continue
                            poolJobs.append((statesFilePath, outputFilePath, latticeSize, beta, lambdaZFilePath, batchNumber))
        
        pool.map(CalculateExpectaionValue.multiThreadCalculateExpectationValue, poolJobs)
        finishTime = time.time()
        print("Total time: ", finishTime - startTime)