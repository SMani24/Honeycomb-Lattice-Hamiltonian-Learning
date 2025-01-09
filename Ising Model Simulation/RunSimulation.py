# In the name of God
# SMani24

import multiprocessing as mp
import MonteCarlo
import argparse
import time

NUMBER_OF_ITERATIONS = int(1e5)
NUMBER_OF_SAMPLES = int(1e5)

FLOAT_SAVING_FORMAT = '%.40f'

LATTICE_SIZES = [8]
BETAS = [0.5]
SINGLE_QUBIT_ERROR_PROBABILITIES = [0.0, 0.05, 0.1, 0.15, 0.2]
CONFIG_NUMBER_RANGE = range(1)
BATCH_RANGE = range(0, 30000)

def generate_monte_carlo_jobs():
    jobs = []
    for lattice_size in LATTICE_SIZES:
        for beta in BETAS:
            for single_qubit_error_probability in SINGLE_QUBIT_ERROR_PROBABILITIES:
                for config_number in CONFIG_NUMBER_RANGE:
                    lambda_z_file_path = (
                        f"./LambdaConfigs/latticeSize={lattice_size}/"
                        f"Beta={beta}/"
                        f"singleQubitErrorProbability={single_qubit_error_probability}/"
                        f"VertexLmabdaConfig={config_number}.csv"
                    )
                    jobs.append((
                        lattice_size, 
                        beta, 
                        lambda_z_file_path, 
                        single_qubit_error_probability, 
                        NUMBER_OF_ITERATIONS, 
                        NUMBER_OF_SAMPLES, 
                        config_number
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

    args = parser.parse_args()
    print(args)

    mp.freeze_support()
    pool = mp.Pool(args.thread_number)

    if args.monte_carlo:
        jobs = generate_monte_carlo_jobs()
        print(jobs[0])
        pool.map(MonteCarlo.multi_thread_monte_carlo, jobs)

    finish_time = time.time()
    print(f"Total time = {finish_time - start_time}")    
