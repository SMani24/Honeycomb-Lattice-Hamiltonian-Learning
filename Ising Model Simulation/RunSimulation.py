# In the name of God
# SMani24

import multiprocessing as mp
import NumericExpectationValueCalculator
import TheoreticalExpectationValueCalculator
import os
from typing import List, Tuple
import MonteCarlo
import argparse
import time
#import VertexFlipProbabilityCalculator
import GenerateLambdaConfig

NUMBER_OF_ITERATIONS = int(1e4)
NUMBER_OF_SAMPLES = int(1e4)
RUN_SET = range(10)

FLOAT_SAVING_FORMAT = '%.40f'

LATTICE_SIZES = [8]#, 12, 16, 20, 24, 28, 32]
BETAS = [0.001]
POSITIVE_LAMBDA_FRACTIONS = [0.5]#, 0.6, 0.7, 0.8]
SINGLE_QUBIT_ERROR_PROBABILITIES = [0.0, 0.05, 0.1, 0.15, 0.2]
CONFIG_NUMBER_RANGE = range(1)
BATCH_RANGE = range(0, 30000)
ADD_STATE = False

def generate_monte_carlo_jobs() -> Tuple[int, int, str, int, int, int, int, int, bool, str]:
    #TODO: Add docstring
    jobs = []
    for lattice_size in LATTICE_SIZES:
        for beta in BETAS:
            for q in POSITIVE_LAMBDA_FRACTIONS:
                for run_number in RUN_SET:
                    for configuration_number in CONFIG_NUMBER_RANGE:
                        lambda_configuration_file_path = (
                            f"./lambda_configurations/"
                            f"lattice_size={lattice_size}/"
                            f"q={q}/"
                            f"configuration_number={configuration_number}.csv"
                        )
                        jobs.append((
                            lattice_size, 
                            beta, 
                            lambda_configuration_file_path, 
                            q,
                            run_number, 
                            NUMBER_OF_ITERATIONS, 
                            NUMBER_OF_SAMPLES, 
                            configuration_number
                        ))
    return jobs

def generate_numeric_expectation_value_jobs() -> Tuple[Tuple[int, str, str]]:
    #TODO: Add docstring
    jobs = []
    for lattice_size in LATTICE_SIZES:
        for beta in BETAS:
            for q in POSITIVE_LAMBDA_FRACTIONS:
                for run_number in RUN_SET:
                    for config_number in CONFIG_NUMBER_RANGE:
                        occurrences_file_path = (
                            f"./MCOutput/"
                            f"latticeSize={lattice_size}/"
                            f"Beta={beta}/"
                            f"singleQubitErrorProbability={q}/"
                            f"run_number={run_number}/"
                            f"configNumber={config_number}.csv"
                        )
                        output_file_directory = (
                            f"./ExpectationValues/"
                            f"FinalExpectationValue/"
                            f"latticeSize={lattice_size}/"
                            f"Beta={beta}/"
                            f"singleQubitErrorProbability={q}/"
                            f"run_number={run_number}/"
                            f"configNumber={config_number}_"
                        )
                        vertex_expectation_value_file_path = (
                            output_file_directory + "vertexExpectationValues.csv"
                        )
                        # linkExpectationValuesFilePath: str = outputFilePath + "linkExpectationValues.csv"
                        if (os.path.isfile(occurrences_file_path) is False or 
                            os.path.isfile(vertex_expectation_value_file_path) is True): #or os.path.isfile(linkExpectationValuesFilePath) == True):
                            continue
                        jobs.append((
                            lattice_size,
                            occurrences_file_path,
                            vertex_expectation_value_file_path
                        ))
    
    return jobs

def generate_theoretical_expectation_value_jobs() -> Tuple[Tuple[int, int, str, str, bool]]:
    #TODO: Add docstring
    jobs = []
    for lattice_size in LATTICE_SIZES:
        for beta in BETAS:
            for q in POSITIVE_LAMBDA_FRACTIONS:
                for run_number in RUN_SET:
                    for config_number in CONFIG_NUMBER_RANGE:
                        occurrences_file_path = (
                            f"./MCOutput/"
                            f"latticeSize={lattice_size}/"
                            f"Beta={beta}/"
                            f"singleQubitErrorProbability={q}/"
                            f"run_number={run_number}/"
                            f"configNumber={config_number}.csv"
                        )
                        output_file_directory = (
                            f"./ExpectationValues/"
                            f"FinalExpectationValue/"
                            f"latticeSize={lattice_size}/"
                            f"Beta={beta}/"
                            f"singleQubitErrorProbability={q}/"
                            f"run_number={run_number}/"
                            f"configNumber={config_number}_"
                        )
                        vertex_expectation_value_file_path = (
                            output_file_directory + "vertexExpectationValues.csv"
                        )
                        # linkExpectationValuesFilePath: str = outputFilePath + "linkExpectationValues.csv"
                        if (os.path.isfile(occurrences_file_path) is False or 
                            os.path.isfile(vertex_expectation_value_file_path) is True): #or os.path.isfile(linkExpectationValuesFilePath) == True):
                            continue
                        
                        lambda_configuration_file_path = (
                            f"./lambda_configurations/"
                            f"lattice_size={lattice_size}/"
                            f"q={q}/"
                            f"configuration_number={config_number}.csv"
                        )

                        jobs.append((
                            lattice_size, 
                            beta,
                            lambda_configuration_file_path,
                            occurrences_file_path,
                            vertex_expectation_value_file_path,
                            ADD_STATE
                        ))
    
    return jobs

def generate_lambda_configuration_jobs() -> Tuple[int, int, int, str]:
    jobs = []
    for lattice_size in LATTICE_SIZES:
        for q in POSITIVE_LAMBDA_FRACTIONS:
            for configuration_number in CONFIG_NUMBER_RANGE:
                lambda_configuration_file_path = (
                    f"./lambda_configurations/"
                    f"lattice_size={lattice_size}/"
                    f"q={q}/"
                    f"configuration_number={configuration_number}.csv"
                )
                jobs.append((
                    lattice_size,
                    q,
                    0,
                    lambda_configuration_file_path
                ))
    return jobs

if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser("#TODO: add description")

    parser.add_argument(
        "-tn", "--thread-number",
        type=int,
        default=12,
        help="Specifies the number of threads to be used"
    )

    #TODO: Make it so that it would get the parameters as input
    parser.add_argument(
        "-mc", "--monte-carlo",
        action="store_true",
        help="""Runs the monte carlo algorithm with the set
        parameters (needs to be changed in code!)"""    
    )
    parser.add_argument(
        "-nve", "--numeric-vertex-expectation-value",
        action="store_true",
        help="""Runs numeric expectation value calculator with parameters
        set in the code"""
    )
    parser.add_argument(
        "-tve", "--theoretical-vertex-expectation-value",
        action="store_true",
        help="""Runs the theoretical vertex expectation value
        calculator with the parameters set in code"""
    )
    parser.add_argument(
        "-vfp", "--vertex-flip-probability",
        action="store_true",
        help="""Calculates vertex flip probability based on the 
        expectation values previously calculated and draws its graph!"""
    )

    parser.add_argument(
        "-glc", "--generate-lambda-configuration",
        action="store_true",
        help="""Generates the lambda_configuration file with the set
        parameters"""
    )

    args = parser.parse_args()
    print(args)

    mp.freeze_support()
    pool = mp.Pool(args.thread_number)

    if args.monte_carlo:
        #TODO: make it so it only produces jobs that are not already done!
        jobs = generate_monte_carlo_jobs()
        pool.map(MonteCarlo.multi_thread_monte_carlo, jobs)

    if args.numeric_vertex_expectation_value:
        #TODO: make it so that in only produces jobs that are not already done!
        jobs = generate_numeric_expectation_value_jobs()
        pool.map(NumericExpectationValueCalculator.multithread_run, jobs)

    if args.theoretical_vertex_expectation_value:
        #TODO: make it so that in only produces jobs that are not already done!
        jobs = generate_theoretical_expectation_value_jobs()
        print(jobs)
        pool.map(TheoreticalExpectationValueCalculator.multithread_run, jobs)

    if args.vertex_flip_probability:
        #TODO: make it so it takes whether or not to save the data as input
        VertexFlipProbabilityCalculator.calculate_vertex_flip_probability(
            BETAS=BETAS,
            LATTICE_SIZE=LATTICE_SIZES,
            CONFIG_RANGE=CONFIG_NUMBER_RANGE,
            SINGLE_QUBIT_PROBABILITIES=SINGLE_QUBIT_ERROR_PROBABILITIES,
            RUN_SET=RUN_SET
        )

    if args.generate_lambda_configuration:
        jobs = generate_lambda_configuration_jobs()
        pool.map(GenerateLambdaConfig.multithread_run, jobs)
    finish_time = time.time()
    print(f"Total time = {finish_time - start_time}")    
