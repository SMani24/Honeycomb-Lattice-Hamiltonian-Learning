import HoneyComb
import math
import random
import matplotlib.pyplot as plt
import csv

def saveData(data, filePath):
    with open(f"./{filePath}.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow(item)
    file.close()

def probabiltyOfSimulatedAnnealing(initialEnergy, postEnergy, T):
    if postEnergy <= initialEnergy:
        return 1
    return math.exp(-(postEnergy - initialEnergy) / T)

def MonteCarlo(latticeSize, beta, lambdaZFilePath="", 
               numOfItertions=10000, numOfSamples=1000):
    T = 10000
    lattice = HoneyComb.HoneyComb(latticeSize=latticeSize, beta=beta,
                                       lambdaZFilePath=lambdaZFilePath)
    currentEnergy = lattice.calculateEnergy()
    probabilities = []
    eneregies = []
    states = []
    for iteration in range(numOfItertions + numOfSamples):
        # print(f"T = {T}, probabilty = {currentStatetProbablity}")
        T = max(T - 10, 1)
        vertex = lattice.selectRandomVertex()
        # Entering the new state
        lattice.applyStabilizerOperatorA(vertex)
        newEnergy = lattice.calculateEnergy()
        currentStatetProbablity = probabiltyOfSimulatedAnnealing(currentEnergy, newEnergy, T)
        randomNumber = random.random()
        if randomNumber < (1 - currentStatetProbablity):
            # Reversing our actions to get back to the original state
            lattice.applyStabilizerOperatorA(vertex)
        else:
            currentEnergy = newEnergy
        
        if iteration >= numOfItertions:
            print(lattice.generateStateString())
            states.append(lattice.generateStateString())
        else:
            eneregies.append(currentEnergy)
            probabilities.append(currentStatetProbablity)
    saveData(states, "test")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  

    ax1.plot(list(range(numOfItertions)), eneregies, label="energies", color='g')             # Line plot of y vs. x
    ax2.plot(list(range(numOfItertions)), probabilities, label="probabilties")
    
    plt.tight_layout()  # Adjust subplots to fit into the figure area.
    plt.show()

MonteCarlo(4, 0.5, "./VertexLmabdaConfig=4.csv")