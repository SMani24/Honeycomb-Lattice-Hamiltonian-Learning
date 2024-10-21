# In the name of God
# SMani24

import base64
from typing import List
import zlib
import numpy as np
import csv
import ast
import os

class Numeration:
    def __init__(self, latticeSize):
        self.linkCount = 3 * (latticeSize * latticeSize)
        self.vertexCount = 2 * (latticeSize * latticeSize)
        self.plaquetteCount = latticeSize * latticeSize

        numerationFile = "../MonteCarlo/Numeration/"
        vertexToLinkFilePath = numerationFile + f"LatticeSize={latticeSize}_vertexToLink.csv"
        linkToVertexFilePath = numerationFile + f"LatticeSize={latticeSize}_linkToVertex.csv"
        plaquetteToVertexFilePath = numerationFile + f"LatticeSize={latticeSize}_plaquetteToVertex.csv"
        plaquetteToLinkFilePath = numerationFile + f"LatticeSize={latticeSize}_plaquetteToLink.csv"
        vertexToPlaquetteFilePath = numerationFile + f"LatticeSize={latticeSize}_vertexToPlaquette.csv"
        linkToPlaquetteFilePath = numerationFile + f"LatticeSize={latticeSize}_linkToPlaquette.csv"

        self.vertexToLink = self.__loadFile(vertexToLinkFilePath)
        self.linkToVertex = self.__loadFile(linkToVertexFilePath)
        self.plaquetteToLink = self.__loadFile(plaquetteToLinkFilePath)
        self.plaquetteToVertex = self.__loadFile(plaquetteToVertexFilePath)
        self.vertexToPlaquette = self.__loadFile(vertexToPlaquetteFilePath)
        self.linkToPlaquette = self.__loadFile(linkToPlaquetteFilePath)

    def __loadFile(self, filePath):
        myDict = dict()
        with open(filePath) as csv_file:
            reader = csv.reader(csv_file)
            for key, value in reader:
                key = int(key)
                value = ast.literal_eval(value)
                myDict[key] = value
        return myDict

def loadData(filePath, dtype=str):
    data = np.genfromtxt(filePath, delimiter=',', dtype=dtype)
    return data

def calculateOccurrences(states):
    """
        Calculates how many of each state we have in the given list of states
    """
    occurrences = dict()
    for state in states:
        if not state in occurrences:
            occurrences[state] = 0
        occurrences[state] += 1
    return occurrences

def applySigmaX(linkId, state):
    """
        Applies the sigmaX pauli operator to the given link (and outputs a new state)
    """
    # Finding the char numbers to be changed
    linkSpinPos = 2 * linkId
    linkPhasePos = 2 * linkId + 1
    newSpin = ""
    if state[linkSpinPos] == "1":
        newSpin = "0"
    else:
        newSpin = "1"

    # Calculating the new state:
    newState = state[:linkSpinPos] + newSpin + state[linkSpinPos + 1:]

    return newState

def getPhase(phaseChar):
    if phaseChar == '0':
        return -1
    elif phaseChar == '1':
        return 1
    else:
        raise ValueError("Unvalid char")

def applySigmaZ(linkId, state):
    """
        Applies the sigmaZ pauli operator to the given link and returns the new Phase
    """
    linkSpinPos = 2 * linkId
    linkPhasePos = 2 * linkId + 1
    if state[linkSpinPos] == "0":
        return getPhase(state[linkPhasePos])
    else:
        phase = getPhase(state[linkPhasePos])
        phase *= -1
        return phase

def applyStabilizerOperatorA(vertexId, state, numeration):
    """
        Applies the operator A on the vertex with id "vertexId"
        Note: Can be improved!!!
    """
    linkIds = numeration.vertexToLink[vertexId]
    newState = state
    for linkId in linkIds:
        newState = applySigmaX(linkId, newState)
    return newState

def saveData(filePath: str, data, format='%s', delimiter=',') -> None:
    # Making the necessery directories:
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    if type(data) != list or type(data) != tuple:
        data = [data]
    data = np.array(data)
    np.savetxt(filePath, data, delimiter=delimiter, fmt=format)

    del data

def convertFromZlibToBase64(compressedString: bytes) -> str:
    """
        Converts the compressedString with zlib library to a 
        base64 text friendly format
    """
    return base64.b64encode(compressedString).decode('utf-8')

def convertFromBase64ToZlib(compressedString: str) -> bytes:
    """
        Converts the encoded data with Base64 to zlib format
    """
    decodedData: bytes = base64.b64decode(compressedString)
    string: str = zlib.decompress(decodedData).decode('utf-8')
    return zlib.compress(string.encode())

def saveCompressedData(filePath: str, compressedData: List[bytes]):
    """
        Saves the data(states) that are compressed using the zlib library
    """
    with open(filePath, mode='w', newline='') as outputFile:
        writer = csv.writer(outputFile)
        for compressedString in compressedData:
            compressedString = convertFromZlibToBase64(compressedString)
            writer.writerow([compressedString])

def loadCompressedData(filePath: str) -> List[bytes]:
    """
        Loads the data encoded with base64 and returns the 
        states compressed with zlib!
    """
    compressedData: List[bytes] = []
    with open(filePath, mode='r') as inputFile:
        reader: csv._reader = csv.reader(inputFile)
        for row in reader:
            zlibCompressedState: bytes = row[0]
            compressedData.append(zlibCompressedState)
    return compressedData