# In the name of God
# SMani24

import os
import sys
from typing import Iterable, List

from matplotlib import pyplot as plt
# parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
# sys.path.append(parent_dir)
import HoneyComb
import GenerateLambdaConfig
 

def ideal_vertex_flip_probability_calculator(
    lattice_sizes: Iterable[int],
    positive_lambda_fractions: Iterable[int],
    configuration_range: Iterable[int]
):
    
    lambda_configuration_dir = "./sample_lambda_configuration/"

    plt.xlabel("vertex flip probability")
    plt.ylabel("q")
    
    for lattice_size in lattice_sizes:
        vertex_flip_probability = dict()
        for q in positive_lambda_fractions:
            vertex_flip_probability[q] = 0
            
            for configuration_number in configuration_range:
                lambda_configuration_file_path = (
                    lambda_configuration_dir +
                    f"lattice_size={lattice_size}/"
                    f"q={q}/"
                    f"configuration_number={configuration_number}.csv"
                )
                GenerateLambdaConfig.generate_lambda_config(
                    lattice_size=lattice_size,
                    positive_lambda_fraction=q,
                    negative_lambda_fraction=0,
                    lambda_configuration_file_path=lambda_configuration_file_path,
                )
                lattice = HoneyComb.HoneyCombIsing(
                    lattice_size=lattice_size,
                    beta=0,
                    lambda_z_file_path=lambda_configuration_file_path,
                    initiate_randomly=True
                )
                # print(lattice.print_link_lambdas())
                number_of_vertices_with_error = lattice.calculate_number_of_vertices_with_error()
                vertex_flip_probability[q] += number_of_vertices_with_error
            vertex_flip_probability[q] /= HoneyComb.HoneyCombIsing.number_of_vertices(lattice_size)
            vertex_flip_probability[q] /= len(configuration_range)
        
        x = [x[1] for x in vertex_flip_probability.items()]
        print(x)
        plt.plot(x, positive_lambda_fractions, label=f"lattice_size={lattice_size}")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    lattice_sizes = range(8, 32, 4)
    positive_lambda_fractions = [round(i * 0.1, 1) for i in range(10)] #[0.5, 0.6, 0.7, 0.8]
    configuration_range = range(100)
    ideal_vertex_flip_probability_calculator(
        lattice_sizes=lattice_sizes,
        positive_lambda_fractions=positive_lambda_fractions,
        configuration_range=configuration_range
    )