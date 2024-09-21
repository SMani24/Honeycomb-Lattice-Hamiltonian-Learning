# In the name of God
# SMani24
# Ali Kookani

import Utils
import numpy as np
import matplotlib.pyplot as plt

BETA = [0.5]
LATTICE_SIZE = [8]
CONFIG_RANGE = range(1)
SINGLE_QUBIT_ERROR_PROBABILITIES = [0.0, 0.05, 0.1, 0.15, 0.2]

# Loading the data:

for latticeSize in LATTICE_SIZE:
        vertexCount = 2 * (latticeSize * latticeSize)
        for beta in BETA:
            
            vertexFlipProbability = np.zeros(len(SINGLE_QUBIT_ERROR_PROBABILITIES))
            for configNumber in CONFIG_RANGE:
                for i, singleQubitErrorProbability in enumerate(SINGLE_QUBIT_ERROR_PROBABILITIES):
                    dirPath = f"./ExpectationValues/"
                    filePath = f"latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/"
                    vertex_A_ExpectationValueFilePath = dirPath + filePath + f"vertex_A_ExpectationValue_configNumber={configNumber}.csv"
                    vertex_A_ExpectationValue = Utils.loadData(vertex_A_ExpectationValueFilePath)
                    vertex_A_ExpectationValue = vertex_A_ExpectationValue.astype(float)
                    # print(vertex_A_ExpectationValue)
                    vertexFlipProbability[i] += np.mean(vertex_A_ExpectationValue)
                print(f"Config={configNumber} done!!")
            
            vertexFlipProbability /= len(CONFIG_RANGE)
            # vertexFlipProbability *= 1 / vertexFlipProbability[0]
            vertexFlipProbability = (1 - vertexFlipProbability) / 2
            
            plt.plot(vertexFlipProbability, SINGLE_QUBIT_ERROR_PROBABILITIES, marker='o')
            plt.xlabel("Vertex Flip Probability, p")
            plt.ylabel("Single Qubit Error Probability, er")

            plotFilePath = f"./Plots/Beta={beta}.png"
            plt.savefig(plotFilePath)