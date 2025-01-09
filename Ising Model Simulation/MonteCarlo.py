# In the name of God the benevolent merciful
# SMani24

import os
import sys
from typing import List, Tuple 
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(parent_dir)
#TODO: Move this method of importing Utils to other TODOS!
import Utils
import math
import numpy as np
import HoneyComb

OUTPUT_DIRECTORY = "./MCOutput"

def go_to_next_state(
    previous_energy: int, 
    next_energy: int, 
    beta: int
) -> bool:
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

def monte_carlo(
    lattice_size: int, 
    beta: int, 
    lambda_z_file_path: str = "", 
    single_qubit_error_probability: int = 0, 
    number_of_iteration: int = 100000, 
    number_of_samples: int = 10000,
    sampling_ratio: int =  1, 
    config_number: int = -1,
    plot_energies: bool = False,
    output_directory: str = "./MCOutput"
) -> None:
    #TODO: add a docstring
    if plot_energies:
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
                                beta=beta,
                                T=T):
            lattice.flip_vertex_spin(vertex)
        current_energy = lattice.energy
        if plot_energies:
            energies.append(current_energy)
        if iteration % 10000 == 0:
            # Making a simple progress indicator
            print(f"MC: main iteration progress: config_number={config_number} {int(iteration / number_of_iteration * 100)}")

        if iteration >= number_of_iteration and iteration % sampling_ratio == 0:
            state = lattice.generate_state_compressed_string()
            if not state in states:
                states[state] = 1
            else:
                states[state] += 1

    file_name = f"/latticeSize={lattice_size}/Beta={beta}/\
singleQubitErrorProbability={single_qubit_error_probability}/\
configNumber={config_number}.csv" 
    output_file_path = output_directory + file_name
    Utils.save_dictionary(dictionary=states, output_file_path=output_file_path)

    Utils.plot_2D(
        title="Energie Plot",
        x_label="Iteration number",
        y_label="Energie",
        y_values=energies
    )

    del energies
    del states
    del lattice

def multi_thread_monte_carlo(job: Tuple[int, int, str, int, int, int, int, int, bool, str]):
    (lattice_size,
    beta,
    lambda_z_file_path,
    single_qubit_error_probability,
    number_of_iteration,
    number_of_samples,
    config_number) = job
    sampling_ratio = 1 
    monte_carlo(
        lattice_size=lattice_size,
        beta=beta,
        lambda_z_file_path=lambda_z_file_path,
        single_qubit_error_probability=single_qubit_error_probability,
        number_of_iteration=number_of_iteration,
        number_of_samples=number_of_samples,
        sampling_ratio=sampling_ratio,
        config_number=config_number,
        output_directory=OUTPUT_DIRECTORY       
    )
