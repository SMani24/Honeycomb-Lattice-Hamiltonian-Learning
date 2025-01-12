# In the name of God
# SMani24

from typing import Tuple
import numpy as np
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(parent_dir)
import Utils
import zlib

FLOAT_SAVING_FORMAT = '%.40f'

def flip_spin(
    spin: str
) -> str:
    """
    Given a spin, it would flip it!

    |+> -> |->
    |-> -> |+>
    """
    if spin == '+':
        return '-'
    if spin == '-':
        return '+'

def flip_vertex(
    vertex_number: int,
    compressed_state: bytes
) -> bytes:
    """
    Flips a vertex in the state.

    Given a compressed sate and a vertex number, it would
    decompress the state, flip the corresponding vertex and 
    return the compressed new state.
    """
    state = zlib.decompress(compressed_state).decode()
    new_state = (
        state[:vertex_number] + 
        flip_spin(state[vertex_number]) + 
        state[vertex_number + 1:]
    )
    compressed_new_state = zlib.compress(new_state.encode())
    return compressed_new_state

def calculate_operator_A_expectation_value_for_vertex(
    occurrences: dict,
    vertex_number: int
) -> float:
    """
    Calculates <Ai> for the vertex with number i (vertex_number).

    Given the occurrences of states and a vertex number, it would 
    iterate over all the states, applies <Ai> to them and then 
    calculates the probability based on the following formula:
    Sum(sqrt(state_probability * converted_state_probability))
    """
    vertex_expectation_value = 0
    for state, number_of_occurrences in occurrences.items():
        state_probability = number_of_occurrences / len(occurrences)
        converted_state = flip_vertex(
            vertex_number=vertex_number,
            compressed_state=state
        )
        if converted_state in occurrences:
            converted_state_probability = occurrences[converted_state] / len(occurrences)
            vertex_expectation_value += np.sqrt(state_probability * converted_state_probability)
    return vertex_expectation_value

def calculate_operator_A_expectation_value(
    occurrences: dict,
    lattice_size: int,
) -> np.ndarray:
    """
    Calculates the expectation value, <A>, for all the vertices
    of the lattice.

    Given the states and their occurrences, it would calculate <Ai> 
    for all the vertices by applying <Ai> to all the states and 
    finding how many occurrences it has in the states
    """
    vertex_count = 2 * (lattice_size * lattice_size)

    expectation_values = np.zeros(vertex_count)
    for vertex_number in range(vertex_count):
        print(f"Vertex {vertex_number} Done!")
        expectation_values[vertex_number] = calculate_operator_A_expectation_value_for_vertex(
            occurrences=occurrences,
            vertex_number=vertex_number
        )
    return expectation_values

def run(
    lattice_size: int,
    occurrences_file_path: str,
    vertex_expectation_value_file_path: str
) -> None:
    """
    Runs the calculation of expectation value.

    Loads the input file, runs calculate_operator_A_expectation_value
    and saves the outputs!
    """
    occurrences = Utils.load_dictionary(occurrences_file_path)
    print("Data Loaded succesfully!")
    expectation_values = calculate_operator_A_expectation_value(
        occurrences=occurrences,
        lattice_size=lattice_size
    )

    Utils.saveData(
        filePath=vertex_expectation_value_file_path, 
        data=expectation_values, 
        format=FLOAT_SAVING_FORMAT
    )

    print("Expectation values saved succesfully!")

def multithread_run(
    job: Tuple[int, str, str]
):
    """
    Necessary function to be able to run multiple instances of run
    """
    
    (lattice_size,
    occurrences_file_path,
    vertex_expectation_value_file_path) = job
    run(
        lattice_size=lattice_size,
        occurrences_file_path=occurrences_file_path,
        vertex_expectation_value_file_path=vertex_expectation_value_file_path
    )