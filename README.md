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
│   └── sensitivity plots
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
git clone YOUR_GITHUB_REPOSITORY_URL
cd Expert-Thermal-AI-Assessment
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

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

The generated dataset contains **1,872 records and 16 columns**.

The three input features are:

- TDP (W)
- Air velocity (m/s)
- TIM thermal conductivity (W/m·K)

The prediction targets are:

- Total thermal resistance (°C/W)
- Junction temperature (°C)

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
| Total thermal resistance | Random Forest | 0.00000315 | 0.00001306 | 0.99999986 |
| Total thermal resistance | Gradient Boosting | 0.00021058 | 0.00026995 | 0.99993932 |
| Junction temperature | Random Forest | 0.23702234 | 0.55063157 | 0.99884388 |
| Junction temperature | Gradient Boosting | 0.25095793 | 0.33142438 | 0.99958116 |

Random Forest performs best for total thermal resistance. Gradient Boosting achieves the lower RMSE and higher R² for junction temperature, while Random Forest has slightly lower MAE for that target.

## Analysis

The project includes:

- Pearson correlation analysis
- Feature importance analysis
- One-factor sensitivity analysis
- Sensitivity plots for both prediction targets

The results indicate that air velocity has a strong negative relationship with total thermal resistance, while TDP has a strong positive relationship with junction temperature.

## Engineering Assumptions and Limitations

The thermal calculations use the supplied heat-sink reference parameters and documented engineering assumptions.

Important assumptions include:

- Air flows along the 90 mm heat-sink length.
- Reynolds number uses fin spacing as the characteristic length.
- Fin efficiency and radiation are not included.
- Convective area includes both fin sides, fin tips, and exposed base surface between fins.

The reference report does not fully specify the convection area calculation, and its reported reference values do not directly match the implemented complete resistance calculation. This discrepancy is documented in the technical report rather than being silently adjusted.

The ML models are evaluated against a held-out portion of a simulated dataset. Their performance should not be interpreted as validation against experimental hardware measurements or proof of generalization to unseen physical designs.

## Reports

Additional documentation is available in the `reports/` directory:

- `technical_report.md` – Thermal modelling, dataset generation, ML evaluation, and engineering analysis.
- `task3_ai_feature_proposals.md` – Proposed AI features for engineering software.
- `task4_motivation_and_ownership.md` – Motivation and ownership responses.

## Author

**Sri Sai Santhosh Aryan**

GitHub: https://github.com/saisanthosharyan

LinkedIn: https://www.linkedin.com/in/sri-sai-santhosh-aryan-k-316767280