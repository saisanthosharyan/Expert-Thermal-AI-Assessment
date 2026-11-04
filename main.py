import subprocess
import sys


def run_step(description, command):
    print("\n" + "=" * 60)
    print(description)
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", command],
        check=False
    )

    if result.returncode != 0:
        print(f"\nERROR: {description} failed.")
        sys.exit(result.returncode)

    print(f"\nSUCCESS: {description} completed.")


def main():
    print("EXPERT THERMAL - AI/ML ASSESSMENT PIPELINE")

    run_step(
        "STEP 1: Generate thermal dataset",
        "src.parameter_sweep"
    )

    run_step(
        "STEP 2: Train and evaluate ML models",
        "src.train_models"
    )

    run_step(
        "STEP 3: Perform correlation and sensitivity analysis",
        "src.sensitivity_analysis"
    )

    print("\n" + "=" * 60)
    print("ALL PIPELINE STEPS COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()