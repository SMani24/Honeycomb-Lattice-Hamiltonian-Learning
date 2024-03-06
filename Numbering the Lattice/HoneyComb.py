# In the name of God
# SMani24
# MoeenFJ

class HoneyComb:
    def __init__(self, L) :
        self.L = L
        self.linkCount = 3 * L * L
        self.vertexCount = 2 * L * L
        self.plaquetteCount = L * L
        NumerateLinks(self)
        NumerateVertices(self)
    
    def GetPlaquetteNum(self, coordinate):
        x, y = coordinate
        num = y * self.L + x
        return num
    def GetPlaquetteCoordinate(self, num):
        y = num // self.L
        x = num % self.L
        return (x, y)
    def GetPlaquetteNeighboursByCoordinate(self, coordinate):
        x, y = coordinate
        L = self.L
        if y % 2 == 0: # y is even
            neighbourCoordinates = [
                (x, (y - 1) % L),
                ((x + 1) % L, (y - 1) % L),
                ((x - 1) % L, y),
                ((x + 1) % L, y),
                (x, (y + 1) % L),
                ((x + 1) % L, (y + 1) % L)
            ]
        else: # y is odd
            neighbourCoordinates = [
                ((x - 1) % L, (y - 1) % L),
                (x, (y - 1) % L),
                ((x - 1) % L, y),
                ((x + 1) % L, y),
                ((x - 1) % L, (y + 1) % L),
                (x, (y + 1) % L)
            ]
        neigbourNums = []
        for plaquetteCoordinte in neighbourCoordinates:
            neigbourNum = GetPlaquetteNum(self, plaquetteCoordinte)
            neigbourNums.append(neigbourNum)
        return neigbourNums

    def NumerateLinks(self) :
        L = self.L
        linkCordToNum = dict()
        linkNumToCord = dict()
        linkCnt = 0
        for x in range(L):
            for y in range(L):
                neighbours = GetPlaquetteNeighboursByCoordinate(self, (x, y))
                currentPlaquette = GetPlaquetteNum(self, (x, y))
                for neigbour in neigbours:
                    i = currentPlaquette
                    j = neigbour
                    if i < j:
                        tmp = i
                        i = j
                        j = tmp
                    if (i, j) not in linkCordToNum:
                        linkCordToNum[(i, j)] = linkCnt
                        linkNumToCord[linkCnt] = (i, j)
                        linkCnt += 1
        self.linkCordToNum = linkCordToNum
        self.linkNumToCord = linkNumToCord
    def NumerateVertices(self):
        L = self.L
        vertexCnt = 0
        vertexCordToNum = dict()
        vertexNumToCord = dict()
        for x in range(L):
            for y in range(L):
                currentNum = GetPlaquetteNum(self, (x, y))
                neighbourCords = GetPlaquetteNeighboursByCoordinate(self, (x, y))
                neighbourNums = []
                # getting the neighbours numbers from their coordinates:
                for neighbourCord in neighbourCords:
                    neighbourNum = GetPlaquetteNum(self, neighbourCord)
                    neighbourNums.append(neighbourNum)
                vertices = [
                    [neighbourNums[0], neighbourNums[1], currentNum],
                    [neighbourNums[1], neighbourNums[3], currentNum],
                    [neighbourNums[3], neighbourNums[5], currentNum],
                    [neighbourNums[4], neighbourNums[5], currentNum],
                    [neighbourNums[4], neighbourNums[2], currentNum],
                    [neighbourNums[2], neighbourNums[0], currentNum]
                ]
                # Making the numbering of the vertices unique
                for i in range(len(vertices)):
                    vertices[i].sort()
                    vertexCord = (vertices[i][0], vertices[i][1], vertices[i][2])
                    if vertexCord not in vertexCordToNum:
                        vertexCordToNum[vertexCord] = vertexCnt
                        vertexNumToCord[vertexCnt] = vertexCord
                        vertexCnt += 1
        self.vertexCordToNum = vertexCordToNum
        self.vertexNumToCord = vertexNumToCord