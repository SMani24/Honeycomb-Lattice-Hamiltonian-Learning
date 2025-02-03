# In the name of God

import zlib
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(parent_dir)
import Utils
import numpy as np
from Link import Link
from Vertex import Vertex
from typing import Iterable
from Plaquette import Plaquette

class HoneyCombIsing:
    def __init__(
        self, 
        lattice_size: int, 
        beta: int, 
        lambda_z_file_path: str="",
        initiate_randomly: bool=False
    ) -> None:
        self.__link_count = 3 * (lattice_size * lattice_size)
        self.__vertex_count = 2 * (lattice_size * lattice_size)
        self.__plaquette_count = lattice_size * lattice_size
        self.__beta = beta
        self.__links = []
        self.__vertices = []
        self.__plaquettes = []
        self.__make_lattice_components(lattice_size, lambda_z_file_path)
        self.energy = self.__calculate_whole_lattice_energy()
        self.__convert_to_numpy()
        if initiate_randomly:
            self.__assign_random_spin_configuration()

    def __convert_to_numpy(self) -> None:
        """
            To improve the efficiency of the code, all the arrays
            will be converted to numpy arrays!
        """
        self.__links = np.array(self.__links, dtype=object)
        self.__vertices = np.array(self.__vertices, dtype=object)
        self.__plaquettes = np.array(self.__plaquettes, dtype=object)

    @staticmethod
    def __calculate_partial_lattice_energy(links: Iterable[Link]) -> None:
        """
            Calculates the energy for the given set of links
        """
        partial_energy = 0
        for link in links:
            partial_energy += link.calculate_energy()
        partial_energy = - partial_energy
        return partial_energy

    def __calculate_whole_lattice_energy(self) -> int:
        """
            By iterating over the entire lattice, based on the B2 formula of the
            paper (-Sigma(J * Theta1 * Theta2)) it will calculate the Hamiltonian
            and returns its value
        """
        return self.__calculate_partial_lattice_energy(self.__links)

    def __load_numeration(self, lattice_size: int, 
                          numeration_file_dir: str="./Numeration/") -> None:
        """
            Given the size of the lattice, it will find and load the 
            corresponding numbering stored in the numeration_file_dir
            and loads them to the appropriate place to later be used for 
            initiation of the lattice.
        """
        #TODO: Make it so that it reads the files from the numeration folder and generates them if they don't exist (+ update the description if this is done)!
        vertex_to_link_file_path = numeration_file_dir + f"LatticeSize={lattice_size}_vertexToLink.csv"
        link_to_vertex_file_path = numeration_file_dir + f"LatticeSize={lattice_size}_linkToVertex.csv"
        plaquette_to_link_file_path = numeration_file_dir + f"LatticeSize={lattice_size}_plaquetteToLink.csv"
        plaquette_to_vertex_file_path = numeration_file_dir + f"LatticeSize={lattice_size}_plaquetteToVertex.csv"
        vertex_to_plaquette_file_path = numeration_file_dir + f"LatticeSize={lattice_size}_vertexToPlaquette.csv"
        link_to_plaquette_file_path = numeration_file_dir + f"LatticeSize={lattice_size}_linkToPlaquette.csv"
        
        self.__vertex_to_link = Utils.load_dictionary(vertex_to_link_file_path)
        self.__link_to_vertex = Utils.load_dictionary(link_to_vertex_file_path)
        self.__plaquette_to_link = Utils.load_dictionary(plaquette_to_link_file_path)
        self.__plaquette_to_vertex = Utils.load_dictionary(plaquette_to_vertex_file_path)
        self.__vertex_to_plaquette = Utils.load_dictionary(vertex_to_plaquette_file_path)
        self.__link_to_plaquette = Utils.load_dictionary(link_to_plaquette_file_path)

    def __initiate_components(self, lambda_z_file_path: str) -> None:
        """
            Makes empty vertices, links and plaquettes (creates new objects of
            each class type and adds them to their corresponding list in lattice)
        """            
        lambda_z_config = np.zeros(self.__link_count) # This is an array where i-th value 
                                                   # corresponds to the lambdaZ of i-th link
        if lambda_z_file_path != "":
            lambda_z_config = np.loadtxt(lambda_z_file_path, delimiter=',')
        for link_number in range(self.__link_count):
            self.__links.append(Link(link_number, 
                                     self.__beta, 
                                     lambda_z_config[link_number]))

        for vertex_number in range(self.__vertex_count):
            self.__vertices.append(Vertex(vertex_number)) 
        
        for plaquette_number in range(self.__plaquette_count):
            self.__plaquettes.append(Plaquette(plaquette_number))

    def __set_link_values(self) -> None:
        """
            Iterates over the links of the lattice and adds their 
            neighbouring vertices and plaquettes to them 
        """
        for link in self.__links:
            # Finding the corresponding vertices of a link
            for vertex_number in self.__link_to_vertex[link.number]:
                link.add_vertex(self.__vertices[vertex_number])
            # Finding the corresponding plaquettes of a link
            for plaquette_number in self.__link_to_plaquette[link.number]:
                link.add_plaquette(self.__plaquettes[plaquette_number])
            
    def __set_vertex_values(self) -> None:
        """
            Iterates over the vertices of the lattice and adds their 
            neighbouring links and plaquettes to them 
        """
        for vertex in self.__vertices:
            # Finding the corresponding links of a vertex
            for link_number in self.__vertex_to_link[vertex.number]:
                vertex.add_link(self.__links[link_number])
            # Finding the corresponding plaquettes of a vertex
            for plaquette_number in self.__vertex_to_plaquette[vertex.number]:
                vertex.add_plaquette(self.__plaquettes[plaquette_number])
    
    def __set_plaquette_values(self) -> None:
        """
            Iterates over the plaquettes of the lattice and adds their 
            neighbouring links and vertices to them 
        """
        for plaquette in self.__plaquettes:
            # Finding the corresponding links of a plaquette
            for link_number in self.__plaquette_to_link[plaquette.number]:
                plaquette.add_link(self.__links[link_number])
            # Finding the corresponding vertices of a link
            for vertex_number in self.__plaquette_to_vertex[plaquette.number]:
                plaquette.add_vertex(self.__vertices[vertex_number])

    def __establish_connections(self) -> None:
        """
            Based on the data loaded by __load_numeration, this function will 
            iterate over vertices, links and plaquettes and adds their connections
            (as an attribute of their corresponding classes)
        """
        self.__set_link_values()
        self.__set_vertex_values()
        self.__set_plaquette_values()

    def __delete_numeration(self) -> None:
        del self.__vertex_to_link
        del self.__link_to_vertex
        del self.__plaquette_to_link
        del self.__plaquette_to_vertex
        del self.__vertex_to_plaquette
        del self.__link_to_plaquette

    def __make_lattice_components(self, lattice_size: int, 
                                  lambda_z_file_path: str,
                                  numeration_file_dir: str="./Numeration/") -> None:
        """
            Creates new components (vertices, links and plaquettes) and establishes
            their connections (adjacencies) based on the files in the numeration_file_dir
            directory (and according to the size of the lattice)
        """
        self.__load_numeration(lattice_size=lattice_size,
                               numeration_file_dir=numeration_file_dir)
        self.__initiate_components(lambda_z_file_path=lambda_z_file_path)
        self.__establish_connections()
        self.__delete_numeration()

    def select_random_vertex(self) -> Vertex:
        """
            Returns a random vertex of the lattice
        """
        vertex = np.random.choice(self.__vertices)
        return vertex
    
    def flip_vertex_spin(self, vertex: Vertex) -> None:
        """
            Given a vertex, it would flip its spin and re-
            calculate the energy of the entire lattice
            (In order to re-calculate the energy of the entire
            lattice we only need to re calculate a few links!)
        """
        links_to_be_recalculated = vertex.links
        old_partial_energy = self.__calculate_partial_lattice_energy(links=links_to_be_recalculated)
        vertex.flip()
        new_partial_energy = self.__calculate_partial_lattice_energy(links=links_to_be_recalculated)
        self.energy = self.energy - old_partial_energy + new_partial_energy
    
    def generate_state_compressed_string(self) -> bytes:
        """
            Iterates over all the vertices and returns a  compressed 
            string where the i-th character is the spin of the i-th vertex
        """
        state_string = ''
        for vertex_number in range(self.__vertex_count):
            vertex = self.__vertices[vertex_number]
            state_string += vertex.get_spin_string()

        return zlib.compress(state_string.encode())

    def __assign_random_spin_configuration(self) -> None:
        """
            Makes a random spin configuration for each vertex and 
            assigns the corresponding values to each vertex's spin
        """
        spin_orientation = np.random.choice([-1, 1], self.__vertex_count)
        for index, vertex in enumerate(self.__vertices):
            vertex.set_spin(spin_orientation[index])

    