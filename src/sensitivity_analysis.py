
"""
Correlation and sensitivity analysis for the heat-sink dataset.

Outputs:
- Correlation matrix CSV
- Correlation heatmap
- Six one-factor sensitivity plots
- Sensitivity summary CSV
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


DATASET_PATH = "data/thermal_dataset.csv"
OUTPUT_DIR = "outputs"

INPUTS = [
    "tdp_w",
    "air_velocity_m_s",
    "k_tim_w_mk",
]

TARGETS = [
    "r_total_c_per_w",
    "junction_temperature_c",
]

LABELS = {
    "tdp_w": "TDP (W)",
    "air_velocity_m_s": "Air velocity (m/s)",
    "k_tim_w_mk": "TIM conductivity (W/m.K)",
    "r_total_c_per_w": "Total thermal resistance (°C/W)",
    "junction_temperature_c": "Junction temperature (°C)",
}


def run_sensitivity_analysis():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    data = pd.read_csv(DATASET_PATH)

    # 1. Correlation analysis
    selected_columns = INPUTS + TARGETS
    correlation = data[selected_columns].corr(method="pearson")

    correlation.to_csv(
        os.path.join(OUTPUT_DIR, "correlation_matrix.csv")
    )

    print("\nPEARSON CORRELATION MATRIX")
    print(correlation.round(4))

    plt.figure(figsize=(10, 7))
    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        center=0,
        fmt=".3f",
        linewidths=0.5
    )
    plt.title("Thermal Parameter Correlation Matrix")
    plt.tight_layout()
    plt.savefig(
        os.path.join(OUTPUT_DIR, "correlation_heatmap.png"),
        dpi=300
    )
    plt.close()

    # 2. One-factor sensitivity analysis
    # Average each output while varying one input parameter.
    sensitivity_records = []

    for feature in INPUTS:
        for target in TARGETS:
            grouped = (
                data.groupby(feature)[target]
                .mean()
                .reset_index()
                .sort_values(feature)
            )

            minimum = grouped[target].min()
            maximum = grouped[target].max()
            change = maximum - minimum

            sensitivity_records.append({
                "input_parameter": feature,
                "output_parameter": target,
                "minimum_average": minimum,
                "maximum_average": maximum,
                "absolute_change": change,
            })

            plt.figure(figsize=(8, 5))
            plt.plot(
                grouped[feature],
                grouped[target],
                marker="o"
            )
            plt.xlabel(LABELS[feature])
            plt.ylabel(LABELS[target])
            plt.title(
                f"Effect of {LABELS[feature]} on "
                f"{LABELS[target]}"
            )
            plt.grid(True, alpha=0.3)
            plt.tight_layout()

            filename = f"sensitivity_{feature}_{target}.png"
            plt.savefig(
                os.path.join(OUTPUT_DIR, filename),
                dpi=300
            )
            plt.close()

    sensitivity_df = pd.DataFrame(sensitivity_records)
    sensitivity_df.to_csv(
        os.path.join(OUTPUT_DIR, "sensitivity_summary.csv"),
        index=False
    )

    print("\nONE-FACTOR SENSITIVITY SUMMARY")
    print(sensitivity_df.to_string(index=False))

    print("\nAnalysis completed successfully!")
    print(f"Results saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_sensitivity_analysis()
