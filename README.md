# Expert Thermal – AI/ML Engineering Assessment

## Project Overview

This project explores the application of Machine Learning to heat-sink thermal performance prediction.

A physics-based thermal model is used to generate a dataset by varying three input parameters:

- **TDP:** 30–250 W
- **Air velocity:** 0.5–15 m/s
- **TIM thermal conductivity:** 1–12 W/m·K

Two Machine Learning algorithms, Random Forest and Gradient Boosting, are trained to predict:

1. Total thermal resistance (°C/W)
2. Junction temperature (°C)

The project also includes model evaluation, feature importance, correlation analysis, and sensitivity analysis.

## Technology Stack

- Python 3.12
- NumPy
- Pandas
- SciPy
- Scikit-learn
- Matplotlib
- Seaborn
- Joblib

## Project Structure

```text
Expert-Thermal-AI-Assessment/
│
├── data/
│   └── thermal_dataset.csv
│
├── models/
│   ├── random_forest_r_total_c_per_w.joblib
│   ├── random_forest_junction_temperature_c.joblib
│   ├── gradient_boosting_r_total_c_per_w.joblib
│   └── gradient_boosting_junction_temperature_c.joblib
│
├── outputs/
│   ├── model_metrics.csv
│   ├── feature_importance.csv
│   ├── correlation_matrix.csv
│   ├── correlation_heatmap.png
│   ├── sensitivity_summary.csv
│   └── sensitivity_*.png
│
├── reports/
│   ├── technical_report.md
│   ├── task3_ai_feature_proposals.md
│   └── task4_motivation_and_ownership.md
│
├── src/
│   ├── thermal_model.py
│   ├── parameter_sweep.py
│   ├── train_models.py
│   ├── sensitivity_analysis.py
│   └── __init__.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/saisanthosharyan/Expert-Thermal-AI-Assessment.git
cd Expert-Thermal-AI-Assessment
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

## Run the Project

Execute the complete pipeline:

```bash
python main.py
```

The pipeline performs three stages:

1. Generates the thermal dataset.
2. Trains and evaluates the Machine Learning models.
3. Performs correlation and sensitivity analysis.

Generated datasets, trained models, evaluation metrics, and visualizations are saved in their respective directories.

## Dataset

The generated dataset contains **1,872 records and 16 columns**, with no missing values.

The three input features are:

- TDP (W)
- Air velocity (m/s)
- TIM thermal conductivity (W/m·K)

The prediction targets are:

- Total thermal resistance (°C/W)
- Junction temperature (°C)

Dataset location: `data/thermal_dataset.csv`

## Machine Learning Models

Two regression algorithms are evaluated:

- Random Forest Regressor
- Gradient Boosting Regressor

The models are evaluated using:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

### Model Performance

| Prediction Target | Model | MAE | RMSE | R² |
|---|---|---:|---:|---:|
| Total thermal resistance | Random Forest | 0.00000303 | 0.00001191 | 0.99999989 |
| Total thermal resistance | Gradient Boosting | 0.00019652 | 0.00026358 | 0.99994378 |
| Junction temperature | Random Forest | 0.24825017 | 0.59519512 | 0.99930828 |
| Junction temperature | Gradient Boosting | 0.26615214 | 0.35698529 | 0.99975116 |

Random Forest performs best for total thermal resistance across all three evaluation metrics.

For junction temperature, Gradient Boosting achieves the lower RMSE and higher R², while Random Forest achieves a slightly lower MAE.

### Feature Importance

The Random Forest feature importance results indicate:

**Total thermal resistance:**

- Air velocity: 0.927756
- TIM conductivity: 0.072242
- TDP: 0.000002

**Junction temperature:**

- TDP: 0.923431
- Air velocity: 0.071383
- TIM conductivity: 0.005185

Air velocity is the dominant feature for total thermal resistance, while TDP is the dominant feature for junction temperature.

## Analysis

The project includes:

- Pearson correlation analysis
- Feature importance analysis
- One-factor sensitivity analysis
- Sensitivity plots for both prediction targets

The results indicate that:

- Air velocity has a strong negative correlation with total thermal resistance.
- TDP has a strong positive correlation with junction temperature.
- TIM conductivity has a negative relationship with total thermal resistance.
- TDP does not directly affect the calculated thermal resistance in the implemented model.

These findings describe relationships within the generated simulation dataset.

## Baseline Thermal Calculation

For the baseline inputs:

- TDP: 150 W
- Air velocity: 1 m/s
- TIM conductivity: 4 W/m·K

The implemented thermal model produces:

| Parameter | Result |
|---|---:|
| Junction-to-case resistance | 0.200000°C/W |
| TIM resistance | 0.010582°C/W |
| Convective resistance | 0.158623°C/W |
| Script-defined `R_hs` aggregate | 0.169205°C/W |
| Total thermal resistance | 0.369205°C/W |
| Junction temperature | 80.380740°C |

## Engineering Assumptions and Limitations

The thermal calculations use the supplied heat-sink reference parameters and the calculation logic of the original supplied Python script.

Important implementation details:

- Air flows along the 90 mm heat-sink length.
- Reynolds number uses fin spacing as its characteristic length.
- The laminar Nusselt correlation uses the 90 mm heat-sink length.
- Convective area follows the original script's fin-side and exposed-base area calculation.
- Fin efficiency and thermal radiation are not included.
- The original supplied Python script uses junction-to-case resistance of 0.2°C/W, whereas the reference report specifies 0.1°C/W.
- The original supplied Python script does not calculate base conduction resistance.

The reference report does not fully specify the convection-area calculation, and its reported reference values do not directly match the implemented calculation. The discrepancies and implementation details are documented in the technical report rather than being silently adjusted.

The ML models are evaluated against a held-out portion of a simulation-generated dataset. Their performance should not be interpreted as validation against experimental hardware measurements or proof of generalization to unseen physical designs.

## Reports

Additional documentation is available in the `reports/` directory:

- `technical_report.md` – Thermal modelling, dataset generation, ML evaluation, and engineering analysis.
- `task3_ai_feature_proposals.md` – Proposed AI features for engineering software.
- `task4_motivation_and_ownership.md` – Motivation and ownership responses.

## Author

**Sri Sai Santhosh Aryan**

GitHub: https://github.com/saisanthosharyan