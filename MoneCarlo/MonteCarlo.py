import HoneyComb

def MonteCarlo(latticeSize, beta, lambdaZFilePath="", 
               numOfItertions=100, numOfSamples=0):
    lattice = HoneyComb.HoneyComb(latticeSize=latticeSize, beta=beta,
                                       lambdaZFilePath=lambdaZFilePath)
    hamiltoninan = lattice.calculateHamiltoninan()
    for _ in range(numOfItertions):
        vertex = lattice.selectRandomVertex()
        lattice.applyStabilizerOperatorA(vertex)
        # lattice.printLinks()
        newHamiltoninan = lattice.calculateHamiltoninan()
        print(hamiltoninan)
        if newHamiltoninan <= hamiltoninan:
            hamiltoninan = newHamiltoninan
        else:
            lattice.applyStabilizerOperatorA(vertex)
    print(hamiltoninan)

MonteCarlo(4, 0.1, "./VertexLmabdaConfig=4.csv")