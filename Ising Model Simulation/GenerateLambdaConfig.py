# In the name of God
# SMani24

import os
import sys
from typing import Tuple
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(parent_dir)
import Utils
import numpy as np
from HoneyComb import HoneyCombIsing

def generate_lambda_config(
    lattice_size: int,
    positive_lambda_fraction: float,
    negative_lambda_fraction: float,
    lambda_configuration_file_path: str
) -> None:
    """
    Generates and saves the lambda(error) distribution on the lattice

    This function creates a configuration of lambda values for the links in a lattice,
    where a specified fraction of links are assigned positive and negative lambda values.
    The resulting configuration is saved to a specified file.

    Parameters:
    lattice_size(int): The size of the lattice
    positive_lambda_fraction(float): The fraction of the links that have
    a +1 lambda(error)
    negative_lambda_fraction(float): The fraction of the links that have
    a -1 lambda(error)
    lambda_config_file_path(str): Output file path

    Returns:
    None: This function saves the configuration to a file and does
    not return anything
    """
    link_count = HoneyCombIsing.number_of_links(
        lattice_size=lattice_size
    )
    links = list(range(link_count))

    links_with_positive_error_count = int(link_count * positive_lambda_fraction)
    links_with_positive_error = np.random.choice(
        links, 
        links_with_positive_error_count,
        replace=False
    )
    links = [link for link in links if link not in links_with_positive_error]

    links_with_negative_error_count = int(link_count * negative_lambda_fraction)
    links_with_negative_error = np.random.choice(
        links,
        links_with_negative_error_count,
        replace=False 
    )

    lambda_configuration = np.zeros(link_count)
    for link_number in range(link_count):
        if link_number in links_with_positive_error:
            lambda_configuration[link_number] = 1
        if link_number in links_with_negative_error:
            lambda_configuration[link_number] = -1

    Utils.saveData(
        filePath=lambda_configuration_file_path,
        data=lambda_configuration,
        format='%i'
    )

def multithread_run(job: Tuple[int, int, int, str]) -> None:
    (lattice_size,
    positive_lambda_fraction,
    negative_lambda_fraction,
    lambda_configuration_file_path) = job
    generate_lambda_config(
        lattice_size=lattice_size,
        positive_lambda_fraction=positive_lambda_fraction,
        negative_lambda_fraction=negative_lambda_fraction,
        lambda_configuration_file_path=lambda_configuration_file_path
    )

generate_lambda_config(
    lattice_size=8,
    positive_lambda_fraction=0.5,
    negative_lambda_fraction=0,
    lambda_configuration_file_path="./tst.csv"
)