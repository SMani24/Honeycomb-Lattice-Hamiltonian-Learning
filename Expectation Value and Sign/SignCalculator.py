# In the name of God
# SMani24
# Ali Kookani

import Utils

def calculateLambdaZLinkSign(linkId, occurrences):
    """
        Calculates the sign of lambdaZ for the given link 
        1 for positive and -1 for negative and 0 for 0
    """
    magnitudeSum = 0 
    # Since the denominator of all magnitudes are the same we can only sum the numerator
    for state, numInstances in occurrences.items():
        phase = Utils.applySigmaZ(linkId, state)
        magnitudeSum += phase * numInstances
    if magnitudeSum == 0:
        return 0
    elif magnitudeSum > 0:
        return 1
    elif magnitudeSum < 0:
        return -1 

def calculateLambdaZSigns(occurrences, numeration):
    """
        Calculates the sign of lambdaZ for all the links
    """
    signs = []
    for linkId in range(numeration.linkCount):
        signs.append(calculateLambdaZLinkSign(linkId, occurrences))
    return signs

def run(statesFilePath, signFilePath, latticeSize):
    # Loading the data:
    states = Utils.loadData(statesFilePath)
    numeration = Utils.Numeration(latticeSize)
    occurrences = Utils.calculateOccurrences(states)
    print("occurrences calculated!")
    signs = calculateLambdaZSigns(occurrences, numeration)
    Utils.saveData(signFilePath, signs)
    print("output saved!")

def multithreadRun(job):
    statesFilePath, signFilePath, latticeSize = job
    run(statesFilePath, signFilePath, latticeSize)