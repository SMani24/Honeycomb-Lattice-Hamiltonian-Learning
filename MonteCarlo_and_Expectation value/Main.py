# In the name of God
# SMani24
# Ali Kookani
import multiprocessing as mp
import time
import MonteCarlo
import os

startTime = time.time()

NUMBER_OF_ITERATIONS = 1000000
NUMBER_OF_SAMPELS = 100000

LATTICE_SIZES = [8]
BETAS = [0.5]
SINGLE_QUBIT_ERROR_PROBABILITES = [0.0, 0.05, 0.1, 0.15, 0.2]

if __name__ == "__main__":
    threadNumber = int(input("Enter the number of threades to be used: "))

    mp.freeze_support()
    pool = mp.Pool(threadNumber)
    
    poolJobs = []

    for latticeSize in LATTICE_SIZES:
        for beta in BETAS:
            for singleQubitErrorProbability in SINGLE_QUBIT_ERROR_PROBABILITES:
                for configNumber in range(1):
                    lambdaZFilePath = f"./LambdaConfigs/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/VertexLmabdaConfig={configNumber}.csv"
                    poolJobs.append((latticeSize, beta, lambdaZFilePath, singleQubitErrorProbability, NUMBER_OF_ITERATIONS, NUMBER_OF_SAMPELS, configNumber))

    pool.map(MonteCarlo.multithreadMonteCarlo, poolJobs)
    finishTime = time.time()
    print("Total time: ", finishTime - startTime)