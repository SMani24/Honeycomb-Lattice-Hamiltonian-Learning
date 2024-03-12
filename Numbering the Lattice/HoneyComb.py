# In the name of God
# SMani24
# MoeenFJ

class HoneyComb:
    def __init__(self, L) :
        """Note that our assumption of two plaquettes haveing only
          one common link doesn't hold for 2x2 Lattice"""
        self.L = L
        self.linkCount = 3 * L * L
        self.vertexCount = 2 * L * L
        self.plaquetteCount = L * L
        self.NumerateLinks()
        self.NumerateVertices()
    
    def GetPlaquetteNum(self, coordinate):
        x, y = coordinate
        num = y * self.L + x
        return num
    def GetPlaquetteCoordinate(self, num):
        y = num // self.L
        x = num % self.L
        return (x, y)
    def GetPlaquetteNeighboursNumByCoordinate(self, coordinate):
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
            neigbourNum = self.GetPlaquetteNum(plaquetteCoordinte)
            neigbourNums.append(neigbourNum)
        return neigbourNums

    def NumerateLinks(self) :
        L = self.L
        linkCordToNum = dict()
        linkNumToCord = dict()
        linkCnt = 0
        for y in range(L):
            for x in range(L):
                neighbours = self.GetPlaquetteNeighboursNumByCoordinate((x, y))
                currentPlaquette = self.GetPlaquetteNum((x, y))
                print(currentPlaquette)
                print(neighbours)
                for neigbour in neighbours:
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
                currentNum = self.GetPlaquetteNum((x, y))
                neighbourNums = self.GetPlaquetteNeighboursNumByCoordinate((x, y))
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