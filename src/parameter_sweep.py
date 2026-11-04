"""
Generate a thermal performance dataset by varying:
1. Processor TDP
2. Air velocity
3. TIM thermal conductivity

The thermal calculations are performed using thermal_model.py.
"""

import itertools
import pandas as pd

from src.thermal_model import calculate_thermal_performance


def generate_dataset():

    # Input ranges specified in the assessment
    tdp_values = [
        30, 50, 70, 90, 110,
        130, 150, 170, 190, 210,
        230, 250
    ]

    air_velocity_values = [
        0.5, 1, 2, 3, 4,
        5, 6, 7, 8, 9,
        10, 12, 15
    ]

    tim_conductivity_values = [
        1, 2, 3, 4, 5, 6,
        7, 8, 9, 10, 11, 12
    ]

    records = []

    # Generate every possible combination
    combinations = itertools.product(
        tdp_values,
        air_velocity_values,
        tim_conductivity_values
    )

    for tdp, velocity, k_tim in combinations:

        result = calculate_thermal_performance(
            tdp_w=tdp,
            air_velocity_m_s=velocity,
            k_tim_w_mk=k_tim
        )

        records.append(result)

    # Convert results into a DataFrame
    dataset = pd.DataFrame(records)

    # Save CSV
    output_path = "data/thermal_dataset.csv"

    dataset.to_csv(output_path, index=False)

    print("\nDataset generated successfully!")
    print("-----------------------------------")
    print(f"Total records: {len(dataset)}")
    print(f"Total columns: {len(dataset.columns)}")
    print(f"Saved to: {output_path}")

    print("\nFirst five records:")
    print(dataset.head())

    print("\nDataset information:")
    print(dataset.describe())

    return dataset


if __name__ == "__main__":
    generate_dataset()