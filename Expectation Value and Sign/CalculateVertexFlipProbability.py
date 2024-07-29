# In the name of God
# SMani24
# Ali Kookani

import Utils
import numpy as np
import matplotlib.pyplot as plt

BETA = [0.5]
LATTICE_SIZE = [8]
CONFIG_RANGE = range(0, 1000)
SINGLE_QUBIT_ERROR_PROBABILITIES = [0.05, 0.1, 0.15, 0.2]

# Loading the data:

for latticeSize in LATTICE_SIZE:
        for beta in BETA:
            
            for configNumber in CONFIG_RANGE:
                vertexFlipProbability = []
                for singleQubitErrorProbability in SINGLE_QUBIT_ERROR_PROBABILITIES:
                    dirPath = f"./ExpectationValues/"
                    filePath = f"latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/"
                    vertex_A_ExpectationValueFilePath = dirPath + filePath + f"vertex_A_ExpectationValue_configNumber={configNumber}.csv"
                    vertex_A_ExpectationValue = Utils.loadData(vertex_A_ExpectationValueFilePath)
                    vertex_A_ExpectationValue = vertex_A_ExpectationValue.astype(float)
                    print(vertex_A_ExpectationValue)
                    vertex_A_ExpectationValue = (1 - vertex_A_ExpectationValue) / 2
                    vertexFlipProbability.append(np.mean(vertex_A_ExpectationValue))
                
                plt.plot(vertexFlipProbability, SINGLE_QUBIT_ERROR_PROBABILITIES)
                plt.xlabel("Vertex Flip Probability, p")
                plt.ylabel("Single Qubit Error Probability, er")

                plotFilePath = "./Plots/Bet={beta}.png"
                plt.savefig(plotFilePath)