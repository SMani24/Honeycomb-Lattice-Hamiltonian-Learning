import HoneyComb

def MonteCarlo(latticeSize, beta, numOfItertions=100, numOfSamples=0):
    lattice = HoneyComb.HoneyComb(latticeSize=latticeSize, beta=beta)
    hamiltoninan = lattice.calculateHamiltoninan()
    for _ in range(numOfItertions):
        vertex = lattice.applyAOnRandomVertex()
        newHamiltoninan = lattice.calculateHamiltoninan()
        print(newHamiltoninan)
        if newHamiltoninan < hamiltoninan:
            pass
        else:
            lattice.applyStabilizerOperatorA(vertex)
    print(hamiltoninan)

MonteCarlo(4, 0.1)