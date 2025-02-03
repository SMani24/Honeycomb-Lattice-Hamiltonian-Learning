# In the name of God
# SMani24

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(parent_dir)
import Utils
import numpy as np
import matplotlib.pyplot as plt

def calculate_vertex_flip_probability(
    BETAS,
    LATTICE_SIZE,
    CONFIG_RANGE,
    SINGLE_QUBIT_PROBABILITIES
):
    for lattice_size in LATTICE_SIZE:
        for beta in BETAS:
            vertex_flip_probability = np.zeros(len(SINGLE_QUBIT_PROBABILITIES))
            for config_number in CONFIG_RANGE:
                for i, single_qubit_probability in enumerate(SINGLE_QUBIT_PROBABILITIES):
                    expectation_value_directory = (
                        f"./ExpectationValues/"
                        f"FinalExpectationValue/"
                    )
                    expectation_value_file_path = (
                        expectation_value_directory + 
                        f"latticeSize={lattice_size}/"
                        f"Beta={beta}/"
                        f"singleQubitErrorProbability={single_qubit_probability}/"
                        f"configNumber={config_number}_vertexExpectationValues.csv"
                    )
                    vertex_A_expectation_values = Utils.loadData(
                        filePath=expectation_value_file_path
                    )
                    vertex_A_expectation_values = vertex_A_expectation_values.astype(float)
                    vertex_flip_probability[i] += np.mean(vertex_A_expectation_values)

            vertex_flip_probability /= len(CONFIG_RANGE)
            print(vertex_flip_probability)
            vertex_flip_probability = (1 - vertex_flip_probability) / 2
            print(vertex_flip_probability)
            Utils.plot_2D(
                title=(
                    f"The relation between single qubit"
                    f"error rate and vertex flip rate"
                ),
                x_label="Vertex Flip Probability, p",
                y_label="Single Qubit Error Probability, er",
                y_values=SINGLE_QUBIT_PROBABILITIES,
                x_values=vertex_flip_probability
            )
