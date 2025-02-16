# In the name of God
# SMani24

import math
import Utils
#TODO: Use the Utils in the main directory!
import random
import HoneyComb
# import matplotlib.pyplot as plt

MIN_T = 0.3
NUMBER_OF_STATES_IN_EACH_FILE = int(1e4)

OUTPUT_DIR = f"./ExpectationValues/"

def probabilityOfSimulatedAnnealing(initialEnergy, postEnergy, T):
    if postEnergy <= initialEnergy:
        return 1
    return math.exp(-(postEnergy - initialEnergy) / T)

def addOneMoreLayer(lattice, states, probabilitySum):
    newStates = dict()
    statesCopy = states.copy()
    cnt = 0
    for vertex in lattice.getVertices():
        print(f"{cnt} Vertices Done!")
        cnt += 1
        for stateNumber, state in enumerate(statesCopy):
            if stateNumber % 10000 == 0:
                print(f"{stateNumber} states Done!, len(states)={len(states)}")
            lattice.loadState(state)
            lattice.applyStabilizerOperatorA(vertex)
            newState = lattice.generateStateString()
            if not newState in states:
                states.add(newState)
                probabilitySum += lattice.getProbability()
            # if not ((newState in states) or (newState in newStates)):
            #     newStates[newState] = lattice.getProbability()

    # for state, probability in newStates.items():
    #     if not state in states:
    #         states.add(state)
    #         probabilitySum += probability
    
    del statesCopy
    del newStates
    return probabilitySum

def MonteCarlo(latticeSize, beta, lambdaZFilePath="", singleQubitErrorProbability=0, 
               numOfItertions=100000, numOfSamples=10000, configNumber=-1):
    T = 10000
    TDiffrence = T / (80 / 100 * numOfItertions)
    print(TDiffrence)
    lattice = HoneyComb.HoneyComb(latticeSize=latticeSize, beta=beta,
                                       lambdaZFilePath=lambdaZFilePath)

    currentEnergy = lattice.energy
    probabilitySum = 0
    probabilities = []
    energies = []
    states = set()
    for iteration in range(numOfItertions + numOfSamples):
        # print(f"T = {T}, probabilty = {currentStatetProbablity}")
        T = max(T - TDiffrence , MIN_T)
        vertex = lattice.selectRandomVertex()
        # Entering the new state
        lattice.applyStabilizerOperatorA(vertex)
        newEnergy = lattice.energy
        currentStateProbability = probabilityOfSimulatedAnnealing(currentEnergy, newEnergy, T)
        randomNumber = random.random()
        if randomNumber < (1 - currentStateProbability):
            # Reversing our actions to get back to the original state
            # print("OH NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            lattice.applyStabilizerOperatorA(vertex)
        else:
            currentEnergy = newEnergy
            state = lattice.generateStateString()
            if (iteration >= numOfItertions) and (not state in states):
                states.add(state)
                probabilitySum += lattice.getProbability()

        if iteration >= numOfItertions:
            # print(lattice.generateStateString())
            # states.append(lattice.generateStateString())
        #     energies.append(currentEnergy)
        #     probabilities.append(currentStateProbability)
            pass
        # else:
        #     energies.append(currentEnergy)
        #     probabilities.append(currentStateProbability)
        
        if iteration % 10000 == 0:
            print(f"MC progress: ConfigNum = {configNumber} progress: {int(iteration / (numOfItertions + numOfSamples) * 100)}%")
    # filePath = f"./MCOutput/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/configNumber={configNumber}"
    
    # Adding more layers of states:
    for _ in range(2):
        probabilitySum = addOneMoreLayer(lattice, states, probabilitySum)

    lattice.setAmplitudeDenominator(probabilitySum ** 0.5)
    
    probabilitySumFilePath = filePath = f"./MCOutput/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/configNumber={configNumber}/ProbabilitySum.csv"
    Utils.saveData(filePath=probabilitySumFilePath, data=f"{probabilitySum:.40f}")

    tmpStates = []
    batch = 0
    for idx, state in enumerate(states):
        if idx % NUMBER_OF_STATES_IN_EACH_FILE == 0:
            if len(tmpStates) > 1:
                filePath = f"./MCOutput/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/configNumber={configNumber}/Batch={batch}.csv"
                batch += 1
                Utils.saveCompressedData(filePath, tmpStates)
            tmpStates = []
        tmpStates.append(state)
    
    if len(tmpStates) > 1:
        filePath = f"./MCOutput/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/configNumber={configNumber}/Batch={batch}.csv"
        batch += 1
        Utils.saveCompressedData(filePath, tmpStates)
    
    # filePath = f"latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/"
    # statesNumberFilePath = OUTPUT_DIR + filePath + f"numberOfStates_configNumber={configNumber}.csv"
    # vertex_A_ExpectationValueFilePath = OUTPUT_DIR + filePath + f"vertex_A_ExpectationValue_configNumber={configNumber}.csv"
    # link_A_ExpectationValueFilePath = OUTPUT_DIR + filePath + f"link_A_ExpectationValue_configNumber={configNumber}.csv"
    # print(filePath)
    # saveData(vertexExpectationValues, vertex_A_ExpectationValueFilePath)
    # print("Vertex expectation values saved!")
    # saveData(linkExpectationValues, link_A_ExpectationValueFilePath)
    # print("Link expectation values saved")
    # saveData([len(states)], statesNumberFilePath)
    # print(statistics.variance(energies))
    # saveData(states, filePath + ".csv")

    # fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  

    # ax1.plot(list(range(numOfItertions + numOfSamples)), energies, label="energies", color='g')             # Line plot of y vs. x
    # ax2.plot(list(range(numOfItertions + numOfSamples)), probabilities, label="probabilties")
    
    # plt.tight_layout()  # Adjust subplots to fit into the figure area.
    # plt.show()
    # plt.savefig(filePath + ".png")
    del states
    del energies
    del tmpStates
    del probabilities


def multithreadMonteCarlo(job):
    latticeSize, beta, lambdaZFilePath, singleQubitErrorProbability, numOfItertions, numOfSamples, configNumber = job
    MonteCarlo(latticeSize, beta, lambdaZFilePath, singleQubitErrorProbability, numOfItertions, numOfSamples, configNumber)