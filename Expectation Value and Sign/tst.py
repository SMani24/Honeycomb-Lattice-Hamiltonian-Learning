def applySigmaX(linkIds, state):
    """
        Applies the sigmaX pauli operator to the given link (and outputs a new state)
    """
    # Finding the char numbers to be changed
    linkIds.sort()
    linkSpinPos = []
    linkPhasePos = []
    for linkId in linkIds:
        linkSpinPos.append(2 * linkId)
        linkPhasePos.append(2 * linkId + 1)
    

    # Calculating the new state:
    lastPos = 0
    for spinPos in linkSpinPos:
        print(spinPos)
        newSpin = ""
        if state[spinPos] == "1":
            newSpin = "0"
        else:
            newSpin = "1"
        newState = state[lastPos:spinPos] + newSpin
        lastPos = spinPos + 1
    newState += state[lastPos:]

    return newState

print(applySigmaX([0, 2, 4], "0101010101"))