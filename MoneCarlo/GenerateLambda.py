import os
import random
import HoneyComb
import numpy as np

latticeSize = int(input("Enter lattice size: "))
beta = float(input("Enter beta: "))
singleQubitErrorProbability = (float(input("Enter the probability of chosing a vertex: ")))
numOfLambdaConfigs = int(input("Enter the number of lambda configs to be generated: "))
generateVertexLambda = input("Do you want the VertexLambda to be generated?(Yes/No)")

# latticeSize = 100
# beta = 0.2
# singleQubitErrorProbability = 0.2
# numOfLambdaConfigs = 1
# generateVertexLambda = "y"

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
            chosenLinks[linkNumber] = 1
            numOfChosenLinks += 1
        fileName = f"VertexLmabdaConfig={configNumber}.csv"
        saveFile(chosenLinks, filePath + fileName)

    