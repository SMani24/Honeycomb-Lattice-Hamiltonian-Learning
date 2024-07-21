 

import os
import HoneyComb
import numpy as np
import matplotlib.pyplot as plt

def calculateSingleConfigVertexFlipProbability(latticeSize, beta, lambdaZFilePath, vertexErrorNumber):
    lattice = HoneyComb.HoneyComb(latticeSize, beta, lambdaZFilePath)
    lambdaZErrorList = lattice.generateVertexLambdaZErrorList()
    for vertexNumber, hasError in lambdaZErrorList:
        vertexErrorNumber[vertexNumber] += hasError
    
def calculateAverageVertexFlipProbability(latticeSize, beta, singleQubitErrorProbability, numberOfConfigs=1000):
    linkCount = 3 * (latticeSize * latticeSize)
    vertexCount = 2 * (latticeSize * latticeSize)
    vertexErrorNumber = np.zeros(linkCount)
    for configNumber in range(numberOfConfigs):
        print(configNumber)
        lambdaZFilePath = f"../Lattice/LambdaConfigs/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/VertexLmabdaConfig={configNumber}.csv"
        calculateSingleConfigVertexFlipProbability(latticeSize, beta, lambdaZFilePath, vertexErrorNumber)
    
    vertexErrorProbability = vertexErrorNumber / (numberOfConfigs)
    return np.mean(vertexErrorProbability)

def drawPlot(x, y, outputPath, XLabel='', YLabel='', title=''):
    os.makedirs(os.path.dirname(outputPath), exist_ok=True)
    
    plt.plot(x, y, marker='o')  # `marker='o'` adds circles at each data point

    # Adding labels and title
    plt.xlabel(XLabel)
    plt.ylabel(YLabel)
    plt.title(title)

    # # Display the plot
    # plt.show()

    # Save the plot as a PNG file
    plt.savefig(outputPath, format='png')

def run():
    singleQubitErrorProbabilities = [0, 0.05, 0.1, 0.15, 0.2]
    for latticeSize in [8]:
        for beta in [0.5]:
            vertexFlipProbability = []
            for singleQubitErrorProbability in singleQubitErrorProbabilities:
                print(singleQubitErrorProbability)
                vertexFlipProbability.append(calculateAverageVertexFlipProbability(latticeSize, beta, singleQubitErrorProbability))
            
            plotPath = f"./ProbabilityPlots/latticeSize={latticeSize}/Beta={beta}/simulatedPlot.png"
            drawPlot(singleQubitErrorProbabilities, vertexFlipProbability, plotPath, "singleQubitErrorProbabilities", "vertexFlipProbability", f"simulatedPlot latticeSize={latticeSize}")
            print(plotPath)
run()