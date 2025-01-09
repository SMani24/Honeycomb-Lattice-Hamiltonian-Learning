# In the name of God
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Link import Link
    from Plaquette import Plaquette
class Vertex:
    def __init__(self, vertex_number, spin=1):
        """
             1 is equivalent to |+>
            -1 is equivalent to |->
        """
        self.number = vertex_number
        self.links = []
        self.plaquettes = []
        self.spin = spin

    def add_link(self, link: "Link") -> None:
        """
            Adds a single link to the links of this vertex
        """
        self.links.append(link)

    def add_plaquette(self, plaquette: "Plaquette") -> None:
        """
            Adds a single plaquette to the plaquettes of this vertex
        """
        self.plaquettes.append(plaquette)

    def flip(self) -> None:
        self.spin *= -1

    def get_spin_string(self) -> str:
        """
            Returns the string of the spin of the vertex
             1 is equivalent to |+>
            -1 is equivalent to |->
        """
        if self.spin == 1:
            return '+'
        return '-'