# In the Name of God
# SMani24

class NumerateSquareLattice:
    def __init__(self, lattice_size: int):
        # Setting the values
        self.lattice_size = lattice_size
        
        # Creating the dictionaries
        
        self.numerate_links()

    def numerate_plaquettes(self):
        """
        Assign a unique number to each plaquette based on its coordinates.

        This function stores the mapping of plaquette coordinates to their 
        corresponding numbers in the dictionary `plaquette_coordinate_to_number` 
        and the reverse mapping in `plaquette_number_to_coordinate`. It also 
        counts the total number of plaquettes and stores this count in 
        `self.plaquette_count`.

        Attributes:
            plaquette_count (int): The total number of plaquettes.
            plaquette_coordinate_to_number (dict): Mapping from coordinates to 
                plaquette numbers.
            plaquette_number_to_coordinate (dict): Mapping from plaquette numbers 
                to coordinates.
        """
        plaquette_coordinate_to_number = dict()
        plaquette_number_to_coordinate = dict()
        plaquette_counter = 0
        for x in range(self.lattice_size):
            for y in range(self.lattice_size):
                if not (x, y) in plaquette_coordinate_to_number:
                    plaquette_coordinate_to_number[(x, y)] = plaquette_counter
                    plaquette_number_to_coordinate[plaquette_counter] = (x, y)
                    plaquette_counter += 1

        self.plaquette_count = plaquette_counter
        self.plaquette_coordinate_to_number = plaquette_coordinate_to_number
        self.plaquette_number_to_coordinate = plaquette_number_to_coordinate

    def numerate_links(self):
        link_coordinate_to_number = dict()
        # link_