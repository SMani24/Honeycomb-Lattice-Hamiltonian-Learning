# In the name of God the benevolent merciful
import math
import numpy as np
import HoneyComb

def go_to_next_state(previous_energy: int, 
                     next_energy: int, 
                     beta: int) -> bool:
    """
        Based on the change in the energy, it will return a boolean
        indicating wether or not we should go the next state.
        If the energy difference is less than or equal to zero, 
        then we shall go to the next state, otherwise, we will 
        decide randomly
    """
    energy_difference = next_energy - previous_energy
    if energy_difference <= 0 or np.random.random() <= math.exp(beta * 2 * energy_difference):
        return True
    return False

def monte_carlo(lattice_size: int, 
                beta: int, 
                lambda_z_file_path: str ="", 
                single_qubit_error_probability: int =0, 
                number_of_iteration: int =100000, 
                number_of_samples: int =10000,
                sampling_ratio: int = 1, 
                config_number: int =-1) -> None:
    #TODO: add a docstring
    energies = []
    states = dict()
    lattice = HoneyComb.HoneyCombIsing(lattice_size=lattice_size,
                                       beta=beta,
                                       lambda_z_file_path=lambda_z_file_path)
    current_energy = lattice.energy
    for iteration in range(number_of_iteration + number_of_samples):
        vertex = lattice.select_random_vertex()
        lattice.flip_vertex_spin(vertex)
        new_energy = lattice.energy
        if not go_to_next_state(previous_energy=current_energy,
                                next_energy=new_energy,
                                beta=beta):
            lattice.flip_vertex_spin(vertex)
        current_energy = lattice.energy
        if iteration % 10000 == 0:
            print(f"MC: main iteration progress: config_number={config_number} {int(iteration / number_of_iteration * 100)}")

        if iteration >= number_of_iteration and iteration % sampling_ratio == 0:
            state = lattice.generate_state_compressed_string()
            if not state in states:
                states[state] = 1
            else:
                states[state] += 1


    #TODO: Change state storing to save dict so preserve space
    #TODO: Add Utils (file saving specifically)
    #TODO: Make it multithreaded