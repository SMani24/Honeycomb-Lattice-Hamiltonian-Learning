import HoneyComb
import matplotlib.pyplot as plt

def MonteCarlo(latticeSize, beta, lambdaZFilePath="", 
               numOfItertions=10000, numOfSamples=0):
    lattice = HoneyComb.HoneyComb(latticeSize=latticeSize, beta=beta,
                                       lambdaZFilePath=lambdaZFilePath)
    hamiltoninan = lattice.calculateHamiltoninan()
    eneregies = []
    print(hamiltoninan)
    for _ in range(numOfItertions):
        vertex = lattice.selectRandomVertex()
        # print(f"vertex={vertex.getNumber()}")
        lattice.applyStabilizerOperatorA(vertex)
        # lattice.printLinks()
        newHamiltoninan = lattice.calculateHamiltoninan()
        eneregies.append(-newHamiltoninan)
        # print(newHamiltoninan)
        # if newHamiltoninan >= hamiltoninan:
        #     hamiltoninan = newHamiltoninan
        # else:
        #     lattice.applyStabilizerOperatorA(vertex)
    plt.plot(list(range(numOfItertions)), eneregies)             # Line plot of y vs. x

    # Adding title and labels
    plt.title("Sine Wave")
    plt.xlabel("x values")
    plt.ylabel("sin(x)")
    plt.show()

MonteCarlo(4, 0.5, "./VertexLmabdaConfig=4.csv")