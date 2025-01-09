# In the name of God
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Vertex import Vertex
    from Plaquette import Plaquette
class Link:
    def __init__(self, link_number, beta, lambda_z) -> None:
        self.number = link_number
        self.beta = beta
        self.lambda_z = lambda_z
        self.vertices = []
        self.plaquettes = []

    def add_vertex(self, vertex: "Vertex") -> None:
        """
            Adds a single vertex to the vertices of this link
        """
        self.vertices.append(vertex)

    def add_plaquette(self, plaquette: "Plaquette") -> None:
        """
            Adds a single plaquette to the plaquettes of this link
        """
        self.plaquettes.append(plaquette)

    def calculate_energy(self) -> int:
        """
            The function would return the energy of the link
            (Equation B2 of the paper, J * Theta1 * Theta2)
        """
        Theta1 = self.vertices[0].spin
        Theta2 = self.vertices[1].spin
        self.J = math.sinh(self.lambda_z * self.beta)
        return (self.J * Theta1 * Theta2)