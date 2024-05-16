import os
import random
import HoneyComb
import numpy as np

# latticeSize = int(input("Enter lattice size: "))
# beta = float(input("Enter beta: "))
# probabilityOfChosingLinks = (float(input("Enter the probability of chosing a vertex: ")))
# numOfLambdaConfigs = int(input("Enter the number of lambda configs to be generated: "))
# generateVertexLambda = input("Do you want the VertexLambda to be generated?(Yes/No)")

latticeSize = 4
beta = 0.1
probabilityOfChosingLinks = 0.5
numOfLambdaConfigs = 10
generateVertexLambda = "y"

linkCount = 3 * (latticeSize * latticeSize)
vertexCount = 2 * (latticeSize * latticeSize)
plaquetteCount = latticeSize * latticeSize

# Making sure the file path exist
filePath = f"./LambdaConfigs/latticeSize={latticeSize}/Beta={beta}/"
if not os.path.exists(filePath):
    # Create the directory
    os.makedirs(filePath)

lattice = HoneyComb.HoneyComb(latticeSize=latticeSize, beta=beta)

def saveFile(array, filePath):
    # Save the array to a CSV file
    np.savetxt(filePath, array, delimiter=',', fmt='%d')

if generateVertexLambda.lower() in ["yes", "y"]:
    for configNumber in range(numOfLambdaConfigs):
        numOfChosenLinks = 0
        chosenLinks = np.zeros(linkCount, dtype=int)
        while numOfChosenLinks < probabilityOfChosingLinks * linkCount:
            link = lattice.selectRandomLink()
            if chosenLinks[link.getNumber()] == 1:
                continue

            # Some sort of condition needs to be met
            chosenLinks[link.getNumber()] = 1
            numOfChosenLinks += 1
        fileName = f"VertexLmabdaConfig={configNumber}.csv"
        saveFile(chosenLinks, filePath + fileName)

    