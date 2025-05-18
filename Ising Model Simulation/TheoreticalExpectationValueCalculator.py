# In the name of God
# SMani24

import os
import sys
from typing import Tuple
import Vertex

import numpy as np
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(parent_dir)
import HoneyComb
import Utils

FLOAT_SAVING_FORMAT = '%.40f'

def calculate_operator_A_expectation_value_for_vertex(
    states: dict,
    lattice_size: int,
    beta: int,
    Z: float,
    lambda_z_file_path: str,
    vertex_number: Vertex,
    add_state: bool=False
) -> float:
    """
    Calculates <Ai> for the vertex with number i (vertex_number).

    Given the states of states and a vertex number, it would 
    iterate over all the states, applies <Ai> to them and then 
    calculates the probability based on the following formula:
    Sum(Pi * Pj)
    """
    vertex_expectation_value = 0
    
    lattice = HoneyComb.HoneyCombIsing(
        lattice_size=lattice_size,
        beta=beta,
        lambda_z_file_path= lambda_z_file_path,
    )
    new_states = set()

    for state_number, state in enumerate(states):
        if (state_number % 10000 == 0):
            print(f"State number {state_number} done!")
        lattice.load_state(state)
        previous_amplitude = lattice.get_lattice_amplitude()
        lattice.flip_vertex_spin(
            vertex=vertex_number
        )
        new_amplitude = lattice.get_lattice_amplitude()
        vertex_expectation_value += previous_amplitude * new_amplitude
        new_state = lattice.generate_state_compressed_string()

        if (not new_state in states) and (add_state is True):
            new_states.add(new_state)
        
    for state in new_states:
        states.add(state)
        lattice.load_state(state)
        previous_amplitude = lattice.get_lattice_amplitude()
        lattice.flip_vertex_spin(
            vertex=vertex_number
        )
        new_amplitude = lattice.get_lattice_amplitude()
        vertex_expectation_value += previous_amplitude * new_amplitude
        Z += previous_amplitude * previous_amplitude
    
    return (Z, vertex_expectation_value / Z)

def calculate_operator_A_expectation_value(
    states: dict,
    lattice_size: int,
    beta: int,
    lambda_z_file_path: str,
    add_state: bool=False
) -> np.ndarray:
    """
    Calculates the expectation value, <A>, for all the vertices
    of the lattice.

    Given the states and their states, it would calculate <Ai> 
    for all the vertices by applying Ai to all the states and 
    finding how many states it has in the states, it will also keep
    adding new states if add_states is True
    """
    
    # Calculating Z:
    Z = 0
    lattice = HoneyComb.HoneyCombIsing(
        lattice_size=lattice_size,
        beta=beta,
        lambda_z_file_path=lambda_z_file_path,
    )
    for state in states:
        lattice.load_state(
            state=state
        )
        Z += lattice.get_lattice_probability()

    vertex_count = 2 * (lattice_size * lattice_size)

    expectation_values = np.zeros(vertex_count)
    for vertex_number in range(vertex_count):
        Z, expectation_values[vertex_number] = calculate_operator_A_expectation_value_for_vertex(
            states=states,
            lattice_size=lattice_size,
            beta=beta,
            Z=Z,
            lambda_z_file_path=lambda_z_file_path,
            vertex_number=vertex_number,
            add_state=add_state,
        )
        print(f"Vertex {vertex_number} Done!")
    return expectation_values

def run(
    lattice_size: int,
    beta: int,
    lambda_z_file_path: str,
    occurrences_file_path: str,
    vertex_expectation_value_file_path: str,
    add_state: bool=False
) -> None:
    """
    Runs the calculation of expectation value.

    Loads the input file, runs calculate_operator_A_expectation_value
    and saves the outputs!
    """
    occurrences = Utils.load_dictionary(occurrences_file_path)
    states = set(occurrences.keys())
    print("Data Loaded successfully!")
    expectation_values = calculate_operator_A_expectation_value(
        states=states,
        lattice_size=lattice_size,
        beta=beta,
        lambda_z_file_path=lambda_z_file_path,
        add_state=add_state
    )

    Utils.saveData(
        filePath=vertex_expectation_value_file_path, 
        data=expectation_values, 
        format=FLOAT_SAVING_FORMAT
    )

    print("Expectation values saved successfully!")

def multithread_run(
    job: Tuple[int, int, str, str, str, bool]
) -> None:
    """
    Necessary function to be able to run multiple instances of run
    """
    
    (lattice_size, 
    beta,
    lambda_z_file_path,
    occurrences_file_path,
    vertex_expectation_value_file_path,
    add_state) = job
    run(
        lattice_size=lattice_size,
        beta=beta,
        lambda_z_file_path=lambda_z_file_path,
        occurrences_file_path=occurrences_file_path,
        vertex_expectation_value_file_path=vertex_expectation_value_file_path,
        add_state=add_state
    )