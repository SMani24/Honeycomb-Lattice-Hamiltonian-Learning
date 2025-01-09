# In the name of God

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Vertex import Vertex
    from Link import Link

class Plaquette:
    def __init__(self, plaquette_number):
        self.number = plaquette_number
        self.vertices = []
        self.links = []

    def add_vertex(self, vertex: "Vertex") -> None:
        """
            Adds a single vertex to the vertices of this plaquette
        """
        self.vertices.append(vertex)
        
    def add_link(self, link: "Link") -> None:
        """
            Adds a single link to the links of this laquette
        """
        self.links.append(link)