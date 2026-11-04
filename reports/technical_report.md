# AI-Based Thermal Performance Prediction of a Heat Sink

## 1. Project Overview

The objective of this project is to develop a simulation-based machine-learning system to predict heat-sink thermal performance under different operating conditions.

The system varies three input parameters:

- Processor thermal design power (TDP)
- Air velocity
- Thermal interface material (TIM) thermal conductivity

Two thermal outputs are studied:

- Total thermal resistance (°C/W)
- Junction temperature (°C)

Two regression algorithms, Random Forest and Gradient Boosting, are trained and evaluated.

## 2. Reference Parameters and Assumptions

The supplied thermal reference document provides the following baseline parameters.

| Parameter | Value |
|---|---:|
| Processor die length | 52.5 mm |
| Processor die width | 45 mm |
| Heat-sink length | 90 mm |
| Heat-sink width | 116 mm |
| Base thickness | 2.5 mm |
| Number of fins | 60 |
| Fin thickness | 0.8 mm |
| Fin height | 24.5 mm |
| Aluminium conductivity | 167 W/m·K |
| TIM thickness | 0.1 mm |
| Air conductivity | 0.0262 W/m·K |
| Air kinematic viscosity | 1.57 × 10⁻⁵ m²/s |
| Air Prandtl number | 0.71 |
| Ambient temperature | 25°C |
| Junction-to-case resistance | 0.1°C/W |

### Engineering assumptions used in the implementation

The supplied reference does not fully specify the convection-area calculation or all characteristic-length details. The implementation therefore uses the following explicit assumptions:

1. Air flows along the 90 mm heat-sink length.
2. Reynolds number uses fin spacing as its characteristic length.
3. The laminar Nusselt correlation uses the 90 mm heat-sink length in its length ratio.
4. Convective area includes both fin sides, fin tips, and exposed base surface between fins.
5. Fin efficiency and thermal radiation are not included.

These assumptions are implementation choices and should not be interpreted as additional values supplied by the reference document.

## 3. Dataset Generation

A parameter sweep was performed across the following ranges.

| Input parameter | Minimum | Maximum | Number of values |
|---|---:|---:|---:|
| TDP | 30 W | 250 W | 12 |
| Air velocity | 0.5 m/s | 15 m/s | 13 |
| TIM conductivity | 1 W/m·K | 12 W/m·K | 12 |

Total combinations:

12 × 13 × 12 = **1,872 records**

The generated dataset contains 16 columns, including input parameters, intermediate thermal calculations, component resistances, and prediction targets.

**Dataset location:** `data/thermal_dataset.csv`

Dataset validation confirmed:

- Total records: 1,872
- Total columns: 16
- Missing values: 0

## 4. Thermal Calculation Methodology

The thermal calculation follows the equations described in the supplied reference, with the implementation assumptions listed above.

### Fin spacing

Sf = (W − Nf × tf) / (Nf − 1)

### Reynolds number

Re = V × Sf / ν

### Nusselt number

For laminar flow:

Nu = 1.86 × [Re × Pr × (2 × Sf / L)]^(1/3)

For turbulent flow:

Nu = 0.023 × Re^0.8 × Pr^0.3

### Convective heat-transfer coefficient

h = Nu × k_air / (2 × Sf)

### Thermal interface material resistance

R_TIM = t_TIM / (k_TIM × A_die)

### Base conduction resistance

R_cond = t_base / (k_Al × A_die)

### Convective resistance

R_conv = 1 / (h × A_total)

### Total heat-sink and system resistance

R_hs = R_cond + R_conv

R_total = R_jc + R_TIM + R_hs

### Junction temperature

T_junction = T_ambient + TDP × R_total

## 5. Machine-Learning Implementation

Three input features were used:

- `tdp_w`
- `air_velocity_m_s`
- `k_tim_w_mk`

Two targets were predicted independently:

- `r_total_c_per_w`
- `junction_temperature_c`

### Algorithms

**Random Forest Regressor**

An ensemble of decision trees that combines predictions from multiple trees. It can model nonlinear relationships between thermal input parameters and outputs.

Configuration:
- 200 estimators
- Maximum depth: 12
- Random state: 42

**Gradient Boosting Regressor**

An ensemble method that builds decision trees sequentially, with each new tree improving the previous model's prediction errors.

Configuration:
- 150 estimators
- Learning rate: 0.05
- Maximum depth: 3
- Random state: 42

The dataset was split into 80% training data and 20% testing data, using random state 42.

## 6. Model Evaluation

The models were evaluated using three regression metrics:

- **MAE:** Mean Absolute Error
- **RMSE:** Root Mean Squared Error
- **R²:** Coefficient of Determination

### Evaluation results

| Prediction target | Model | MAE | RMSE | R² |
|---|---|---:|---:|---:|
| Total resistance | Random Forest | 0.00000315 | 0.00001306 | 0.99999986 |
| Total resistance | Gradient Boosting | 0.00021058 | 0.00026995 | 0.99993932 |
| Junction temperature | Random Forest | 0.23702234 | 0.55063157 | 0.99884388 |
| Junction temperature | Gradient Boosting | 0.25095793 | 0.33142438 | 0.99958116 |

### Model comparison

For total thermal resistance, Random Forest achieved the lowest MAE and RMSE and the highest R².

For junction temperature, Gradient Boosting achieved the lowest RMSE and the highest R², while Random Forest achieved a slightly lower MAE.

Therefore:

- Random Forest is selected for total thermal resistance prediction.
- Gradient Boosting is selected for junction temperature prediction.

Both algorithms performed well on the held-out test set from the generated simulation dataset.

## 7. Feature Importance

Feature importance was obtained from the tree-based models.

### Total thermal resistance

| Feature | Random Forest importance |
|---|---:|
| TDP | 0.000002 |
| Air velocity | 0.925696 |
| TIM conductivity | 0.074301 |

Air velocity is the dominant feature for total thermal resistance in this simulation.

### Junction temperature

| Feature | Random Forest importance |
|---|---:|
| TDP | 0.858490 |
| Air velocity | 0.131550 |
| TIM conductivity | 0.009960 |

TDP is the dominant feature for junction temperature.

These findings are consistent with the implemented equations: TDP directly affects junction temperature but does not directly affect the calculated thermal resistance.

## 8. Correlation Analysis

Pearson correlation was used to study linear relationships between input parameters and thermal outputs.

| Input parameter | Total resistance correlation | Junction temperature correlation |
|---|---:|---:|
| TDP | -0.0000 | 0.9276 |
| Air velocity | -0.7973 | -0.2671 |
| TIM conductivity | -0.2157 | -0.0723 |

Observations:

1. TDP has a strong positive correlation with junction temperature.
2. Air velocity has a strong negative correlation with total thermal resistance.
3. TIM conductivity has a negative correlation with total thermal resistance.
4. TDP has approximately zero correlation with total resistance because the implemented resistance calculation is independent of TDP.

Correlation indicates association in the generated dataset and does not independently establish causation.

## 9. Sensitivity Analysis

One-factor sensitivity analysis was performed by grouping the dataset by each input parameter and calculating the average output.

| Input parameter | Output | Minimum average | Maximum average | Absolute change |
|---|---|---:|---:|---:|
| TDP | Total resistance | 0.217269 | 0.217269 | 0.000000 |
| TDP | Junction temperature | 31.518074 | 79.317280 | 47.799206 |
| Air velocity | Total resistance | 0.180615 | 0.314071 | 0.133456 |
| Air velocity | Junction temperature | 50.286109 | 68.969981 | 18.683872 |
| TIM conductivity | Total resistance | 0.209850 | 0.248651 | 0.038801 |
| TIM conductivity | Junction temperature | 54.379054 | 59.811153 | 5.432099 |

The results indicate that:

- TDP has the largest effect on junction temperature.
- Air velocity has the largest effect on total thermal resistance.
- TIM conductivity also influences thermal performance, but its observed average effect is smaller.

These changes represent averages across the other parameter combinations in the dataset, not isolated experimental measurements.

## 10. Reference Comparison and Limitations

The supplied reference report lists:

- Total heat-sink thermal resistance: 0.373043°C/W
- Junction temperature: 80.95652°C

At the baseline inputs of 150 W, 1 m/s air velocity, and 4 W/m·K TIM conductivity, the implemented calculation produced:

- Heat-sink resistance: 0.162528°C/W
- Total resistance, including junction-to-case and TIM resistance: 0.273110°C/W
- Junction temperature: 65.96647°C

The implementation does not reproduce the reference values exactly.

The supplied document does not fully specify the total convection-area calculation. It also leaves some ambiguity around the characteristic length in the Nusselt correlation. Additionally, its reported junction temperature appears to use the reported heat-sink resistance directly, whereas the implemented model adds junction-to-case and TIM resistance.

These differences have not been silently adjusted to force a match. The implemented assumptions and resulting discrepancy are reported transparently.

Other limitations include:

1. The dataset is generated from mathematical thermal calculations rather than experimental hardware measurements.
2. Fin efficiency is not modelled.
3. Thermal radiation is not modelled.
4. Contact resistance beyond the specified junction-to-case and TIM terms is not included.
5. Model evaluation uses a random train-test split from the same parameter grid.
6. The results should not be treated as validated predictions outside the specified input ranges.

## 11. Future Improvements

Potential improvements include:

- Validate the thermal equations against the original calculation script or experimental measurements.
- Include fin efficiency and radiation effects.
- Investigate alternative convection correlations and flow regimes.
- Evaluate models on parameter combinations excluded from training.
- Perform uncertainty and error analysis.
- Add an interactive interface for entering thermal parameters and viewing predictions.
- Explore additional regression models and hyperparameter optimization.

## 12. Project Deliverables

| Deliverable | Location |
|---|---|
| Thermal calculation model | `src/thermal_model.py` |
| Dataset generator | `src/parameter_sweep.py` |
| ML training and evaluation | `src/train_models.py` |
| Sensitivity and correlation analysis | `src/sensitivity_analysis.py` |
| Generated dataset | `data/thermal_dataset.csv` |
| Trained ML models | `models/` |
| Model metrics | `outputs/model_metrics.csv` |
| Feature importance | `outputs/feature_importance.csv` |
| Correlation matrix | `outputs/correlation_matrix.csv` |
| Correlation heatmap | `outputs/correlation_heatmap.png` |
| Sensitivity summary | `outputs/sensitivity_summary.csv` |
| Sensitivity plots | `outputs/sensitivity_*.png` |

## 13. Conclusion

This project demonstrates a complete simulation-based workflow for thermal performance prediction using machine learning.

A dataset of 1,872 operating combinations was generated, four regression models were trained, and their performance was evaluated using MAE, RMSE, and R². Correlation, feature importance, and sensitivity analyses were also performed.

The results show that Random Forest performed best for total thermal resistance prediction, while Gradient Boosting achieved the strongest RMSE and R² results for junction temperature prediction.

The implementation provides a foundation for AI-assisted thermal engineering analysis. Further validation against experimental measurements and clarification of the reference calculation methodology are necessary before using the predictions for real engineering design decisions.