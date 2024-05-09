# In the name of God
# SMani24
# MoeenFJ
import numpy as np
import csv

class NumerateHoneycomb:
    def __init__(self, L) :
        """Note that our assumption of two plaquettes haveing only
          one common link doesn't hold for 2x2 Lattice"""
        # Setting the value
        self.L = L
        self.linkCount = 3 * L * L
        self.vertexCount = 2 * L * L
        self.plaquetteCount = L * L
        # Generating dicts:
        self.NumerateLinks()
        self.NumerateVertices()
        self.GeneratePlaquetteToVertex()
        self.GeneratePlaquetteToLink()
        self.GenerateLinkToVertex()
        self.GenerateVertexToLink()

        # Saving dicts:
        # self.SaveDict(self.vertexToLink, f"L={L}_vertexToLink")
        # self.SaveDict(self.linkToVertex, f"L={L}_linkToVertex")
        # self.SaveDict(self.plaquetteToLink, f"L={L}_plaquetteToLink")
        # self.SaveDict(self.plaquetteToVertex, f"L={L}_plaquetteToVertex")
        # self.SaveDict(self.vertexToPlaquette, f"L={L}_vertexToPlaquettek")
        # self.SaveDict(self.linkToPlaquette, f"L={L}_linkToPlaquette")
        
    def SaveDict(self, dic, name):
        with open(f'./{name}.csv', 'w') as csv_file:  
            writer = csv.writer(csv_file)
            for key, value in dic.items():
                writer.writerow([key, value])
        csv_file.close()
    def GetPlaquetteNum(self, coordinate):
        """Getting the plaquette's number from its coordinate"""
        x, y = coordinate
        num = y * self.L + x
        return num
    def GetPlaquetteCoordinate(self, num):
        """Getting the plaquette's coordinate from its number"""
        y = num // self.L
        x = num % self.L
        return (x, y)
    def GetPlaquetteNeighboursNumByCoordinate(self, coordinate):
        """Getting the list of the plaquetes neighbours
            intput : plaquettes coordinate
            output : the list of plaquettes neighbours numbers"""
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
        linkToPlaquette = dict()
        linkCnt = 0
        for y in range(L):
            for x in range(L):
                neighbours = self.GetPlaquetteNeighboursNumByCoordinate((x, y))
                currentPlaquette = self.GetPlaquetteNum((x, y))
                for neigbour in neighbours:
                    i = currentPlaquette
                    j = neigbour
                    if i < j:
                        tmp = i
                        i = j
                        j = tmp
                    if (i, j) not in linkCordToNum:
                        linkCordToNum[(i, j)] = linkCnt
                        linkToPlaquette[linkCnt] = (i, j)
                        linkCnt += 1
        self.linkCordToNum = linkCordToNum
        self.linkToPlaquette = linkToPlaquette
    def NumerateVertices(self):
        L = self.L
        vertexCnt = 0
        vertexCordToNum = dict()
        vertexToPlaquette = dict()
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
                        vertexToPlaquette[vertexCnt] = vertexCord
                        vertexCnt += 1
        self.vertexCordToNum = vertexCordToNum
        self.vertexToPlaquette = vertexToPlaquette
    def GeneratePlaquetteToVertex(self):
        plaquetteToVertex = dict()
        for vertex in range(self.vertexCount):
            plaquettes = self.vertexToPlaquette[vertex]
            for plaquette in plaquettes:
                if plaquette not in plaquetteToVertex.keys():
                    plaquetteToVertex[plaquette] = []
                if vertex not in plaquetteToVertex[plaquette]:
                    plaquetteToVertex[plaquette].append(vertex)
        self.plaquetteToVertex = plaquetteToVertex
    def GeneratePlaquetteToLink(self):
        plaquetteToLink = dict()
        for link in range(self.linkCount):
            plaquettes = self.linkToPlaquette[link]
            for plaquette in plaquettes:
                if plaquette not in plaquetteToLink.keys():
                    plaquetteToLink[plaquette] = []
                if link not in plaquetteToLink[plaquette]:
                    plaquetteToLink[plaquette].append(link)
        self.plaquetteToLink = plaquetteToLink
    def GenerateLinkToVertex(self):
        LinkToVertex = dict()
        for link in range(self.linkCount):
            plaquette1, plaquette2 = self.linkToPlaquette[link]
            vertices1 = set(self.plaquetteToVertex[plaquette1])
            vertices2 = set(self.plaquetteToVertex[plaquette2])
            intersection = vertices1 & vertices2
            LinkToVertex[link] = list(intersection)
        self.linkToVertex = LinkToVertex
    def GenerateVertexToLink(self):
        vertexToLink = dict()
        for link in range(self.linkCount):
            vertices = self.linkToVertex[link]
            for vertex in vertices:
                if vertex not in vertexToLink.keys():
                    vertexToLink[vertex] = []
                vertexToLink[vertex].append(link)
        self.vertexToLink = vertexToLink