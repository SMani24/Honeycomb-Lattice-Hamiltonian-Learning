# In the name of God
# SMani24
# Ali Kookani

import HoneyComb
import statistics
import math
import random
import matplotlib.pyplot as plt
import csv
import numpy as np
import os

def saveData(data, filePath):
    # # print(data)
    # Create the necessary directories
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    data = np.array(data)
    np.savetxt(filePath, data, delimiter=',', fmt='%s')
    # with open(filePath, mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     for item in data:
    #         writer.writerow(item)
    # file.close()

def probabilityOfSimulatedAnnealing(initialEnergy, postEnergy, T):
    if postEnergy <= initialEnergy:
        return 1
    return math.exp(-(postEnergy - initialEnergy) / T)

def MonteCarlo(latticeSize, beta, lambdaZFilePath="", singleQubitErrorProbability=0, 
               numOfItertions=100000, numOfSamples=10000, configNumber=-1):
    T = 10000
    TDiffrence = T / (80 / 100 * numOfItertions)
    print(TDiffrence)
    lattice = HoneyComb.HoneyComb(latticeSize=latticeSize, beta=beta,
                                       lambdaZFilePath=lambdaZFilePath)
    currentEnergy = lattice.energy
    probabilities = []
    energies = []
    states = []
    for iteration in range(numOfItertions + numOfSamples):
        # print(f"T = {T}, probabilty = {currentStatetProbablity}")
        T = max(T - TDiffrence , 0.3)
        vertex = lattice.selectRandomVertex()
        # Entering the new state
        lattice.applyStabilizerOperatorA(vertex)
        newEnergy = lattice.energy
        currentStateProbability = probabilityOfSimulatedAnnealing(currentEnergy, newEnergy, T)
        randomNumber = random.random()
        if randomNumber < (1 - currentStateProbability):
            # Reversing our actions to get back to the original state
            lattice.applyStabilizerOperatorA(vertex)
        else:
            currentEnergy = newEnergy
        
        if iteration >= numOfItertions:
            # print(lattice.generateStateString())
            states.append(lattice.generateStateString())
            # energies.append(currentEnergy)
            # probabilities.append(currentStateProbability)
        # else:
        #     energies.append(currentEnergy)
        #     probabilities.append(currentStateProbability)
        
        if iteration % 10000 == 0:
            print(f"ConfigNum = {configNumber} progress: {int(iteration / (numOfItertions + numOfSamples) * 100)}%")
    filePath = f"./MCOutput/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/configNumber={configNumber}"
    print(filePath)
    # print(statistics.variance(energies))
    saveData(states, filePath + ".csv")

    # fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  

    # ax1.plot(list(range(numOfItertions + numOfSamples)), energies, label="energies", color='g')             # Line plot of y vs. x
    # ax2.plot(list(range(numOfItertions + numOfSamples)), probabilities, label="probabilties")
    
    # plt.tight_layout()  # Adjust subplots to fit into the figure area.
    # plt.show()
    # plt.savefig(filePath + ".png")
    del states
    del energies
    del probabilities

def multithreadMonteCarlo(job):
    latticeSize, beta, lambdaZFilePath, singleQubitErrorProbability, numOfItertions, numOfSamples, configNumber = job
    MonteCarlo(latticeSize, beta, lambdaZFilePath, singleQubitErrorProbability, numOfItertions, numOfSamples, configNumber)