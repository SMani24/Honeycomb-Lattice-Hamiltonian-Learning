# In the name of God
# SMani24

import Utils
import numpy as np
# import matplotlib.pyplot as plt


COEFFICIENT = [12496236.0/12496236.0000000000000000000000000000000000000000
     ,315676959.7183285/70884.4085229309712303802371025085449218750000
     ,8916526036.510366/395.0840357706907184365263674408197402954102
     ,106211989565.94916/17.5810772017357130891923588933423161506653
     ,2946548492870.247/0.0912871431217083806330947481910698115826]

def drawPlot(BETA, LATTICE_SIZE, CONFIG_RANGE, SINGLE_QUBIT_ERROR_PROBABILITIES):
    for latticeSize in LATTICE_SIZE:
            vertexCount = 2 * (latticeSize * latticeSize)
            for beta in BETA:
                
                vertexFlipProbability = np.zeros(len(SINGLE_QUBIT_ERROR_PROBABILITIES))
                for configNumber in CONFIG_RANGE:
                    for i, singleQubitErrorProbability in enumerate(SINGLE_QUBIT_ERROR_PROBABILITIES):
                        dirPath = f"./ExpectationValues/FinalExpectationValue/"
                        filePath = f"latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/"
                        vertex_A_ExpectationValueFilePath = dirPath + filePath + f"vertex_A_ExpectationValue_configNumber={configNumber}.csv"
                        vertex_A_ExpectationValue = Utils.loadData(vertex_A_ExpectationValueFilePath)
                        vertex_A_ExpectationValue = vertex_A_ExpectationValue.astype(float)
                        # print(vertex_A_ExpectationValue)
                        vertexFlipProbability[i] += np.mean(vertex_A_ExpectationValue)
                    print(f"Config={configNumber} done!!")
                
                for i in range(5):
                    vertexFlipProbability[i] *= COEFFICIENT[i]
                print(vertexFlipProbability)

                vertexFlipProbability /= len(CONFIG_RANGE)
                # vertexFlipProbability *= 1 / vertexFlipProbability[0]
                vertexFlipProbability = (1 - vertexFlipProbability) / 2
                print(vertexFlipProbability)
                

                # plt.plot(vertexFlipProbability, SINGLE_QUBIT_ERROR_PROBABILITIES, marker='o')
                # plt.xlabel("Vertex Flip Probability, p")
                # plt.ylabel("Single Qubit Error Probability, er")

                # plotFilePath = f"./Plots/Beta={beta}.png"
                # plt.savefig(plotFilePath)