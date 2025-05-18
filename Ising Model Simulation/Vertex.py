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
        #TODO: Check if it's correct for the spins to be either -1 or 1?
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
    
    def set_spin(self, spin: int | str) -> None:
        """
        Sets the spin of the vertex to the given value, the input
        can either be -1 or 1 or their corresponding string (+, -)
        """
        if type(spin) == str:
            if spin == '+':
                self.spin = 1
            elif spin == '-':
                self.spin = -1
            else:
                raise(f"spin = {spin} is not a valid value")
        else:
            self.spin = spin

    def has_a_link_with_error(self) -> bool:
        """
        Check if the vertex has a link with error

        This Method checks if the vertex has a link with error by
        iterating over all the links of the vertex and checking if 
        they have error or not (using the .has_error method of Link class)

        Returns:
            bool: True if the vertex has a link with error
                  False if the vertex has no links with error
        """
        for link in self.links:
            if link.has_error():
                return True
        return False

    