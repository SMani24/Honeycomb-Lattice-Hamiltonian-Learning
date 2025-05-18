# In the name of God
# SMani24
# Ali Kookani

import os
import random
import HoneyComb
import numpy as np

# latticeSize = int(input("Enter lattice size: "))
# beta = float(input("Enter beta: "))
# singleQubitErrorProbability = (float(input("Enter the probability of chosing a link: ")))
# numOfLambdaConfigs = int(input("Enter the number of lambda configs to be generated: "))
# generateVertexLambda = input("Do you want the VertexLambda to be generated?(Yes/No)")

# latticeSize = 4
# beta = 0.5
# singleQubitErrorProbability = 0.2
# numOfLambdaConfigs = 1000
# generateVertexLambda = "y"

def generateLambda(latticeSize, beta, singleQubitErrorProbability, numOfLambdaConfigs, generateVertexLambda):
    # Making sure the file path exist
    filePath = f"./LambdaConfigs/latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/"
    if not os.path.exists(filePath):
        # Create the directory
        os.makedirs(filePath)

    lattice = HoneyComb.HoneyComb(latticeSize=latticeSize, beta=beta)

    linkCount = lattice.getLinkCount()
    vertexCount = lattice.getVertexCount()
    plaquetteCount = lattice.getPlaquetteCount()

    def saveFile(array, filePath):
        """ 
        Save the array to a CSV file
        """
        np.savetxt(filePath, array, delimiter=',', fmt='%d')

    if generateVertexLambda.lower() in ["yes", "y"]:
        for configNumber in range(numOfLambdaConfigs):
            availableLinkNumbers = list(range(linkCount))
            numOfChosenLinks = 0
            chosenLinks = np.zeros(linkCount, dtype=int)
            while numOfChosenLinks < singleQubitErrorProbability * linkCount:
                linkNumber = random.choice(availableLinkNumbers)
                link = lattice.getLinkByNumber(linkNumber)
                unavailableLinks = list(map(lambda link : link.getNumber(),  link.getAdjacentLinks()))
                # print(f"linkNumber={linkNumber}")
                # print(unavailableLinks)
                # print(availableLinkNumbers)
                for linkNumber in unavailableLinks:
                    if linkNumber in availableLinkNumbers:
                        availableLinkNumbers.remove(linkNumber)
                chosenLinks[linkNumber] = -1
                numOfChosenLinks += 1
            fileName = f"VertexLmabdaConfig={configNumber}.csv"
            saveFile(chosenLinks, filePath + fileName)

numOfLambdaConfigs = 1000
generateVertexLambda = "y"

for latticeSize in [4, 8, 12, 16, 20, 24, 28, 32]:
    for beta in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        for singleQubitErrorProbability in [0, 0.05, 0.1, 0.15, 0.2]: # Can be upto 0.29 (achieved with try and fail)
            generateLambda(latticeSize, beta, singleQubitErrorProbability, numOfLambdaConfigs, generateVertexLambda)
            print(latticeSize, beta, singleQubitErrorProbability)