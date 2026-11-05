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

Two regression algorithms, Random Forest and Gradient Boosting, are trained and evaluated independently for both prediction targets.

The project also includes correlation analysis, feature importance evaluation, and sensitivity analysis to understand how operating parameters influence thermal performance.

## 2. Reference Parameters and Assumptions

The supplied thermal reference document provides the following baseline parameters.

| Parameter | Value |
|---|---:|
| Processor die length | 52.5 mm |
| Processor die width | 45 mm |
| Processor die thickness | 2.2 mm |
| Heat-sink length | 90 mm |
| Heat-sink width | 116 mm |
| Heat-sink height | 27 mm |
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

The supplied reference report specifies junction-to-case resistance as 0.1°C/W. However, the original supplied Python script uses 0.2°C/W. The implementation retains the original Python script's value of **0.2°C/W**.

### Engineering assumptions and implementation details

The supplied reference does not fully specify the convection-area calculation or all characteristic-length details. The implementation follows the original supplied Python code for these calculations.

The following details apply:

1. Air flows along the 90 mm heat-sink length.
2. Reynolds number uses fin spacing as its characteristic length.
3. The laminar Nusselt correlation uses the 90 mm heat-sink length in its length ratio.
4. Convective area follows the area calculation in the supplied Python script.
5. Fin efficiency and thermal radiation are not modelled.
6. Base conduction resistance is not calculated by the original supplied Python script.
7. The junction-to-case resistance is set to 0.2°C/W to match the supplied Python script.

These implementation choices are documented separately from the parameters provided by the reference document.

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

The dataset was generated using the implemented thermal calculation model rather than experimental hardware measurements.

## 4. Thermal Calculation Methodology

The thermal calculation follows the equations and implementation logic of the supplied Python script.

### Fin spacing

\[
S_f = \frac{W-(N_f \times t_f)}{N_f-1}
\]

Where:

- \(W\) is heat-sink width.
- \(N_f\) is the number of fins.
- \(t_f\) is fin thickness.

### Reynolds number

\[
Re = \frac{V \times S_f}{\nu}
\]

Where:

- \(V\) is air velocity.
- \(S_f\) is fin spacing.
- \(\nu\) is air kinematic viscosity.

### Nusselt number

For laminar flow:

\[
Nu = 1.86 \times
\left(Re \times Pr \times \frac{2S_f}{L}\right)^{1/3}
\]

For turbulent flow:

\[
Nu = 0.023 \times Re^{0.8} \times Pr^{0.3}
\]

The implementation uses the transition condition \(Re < 2300\) for laminar flow and the turbulent correlation otherwise.

### Convective heat-transfer coefficient

\[
h = \frac{Nu \times k_{air}}{2S_f}
\]

### Convective area

The implementation calculates fin area as:

\[
A_{fin}=N_f(2 \times h_{fin} \times L)+(S_f \times L)
\]

The exposed base convection area is:

\[
A_{base}=L \times W-(t_f \times N_f \times L)
\]

The total convection area is:

\[
A_{total}=A_{fin}+A_{base}
\]

This reproduces the area calculation in the original supplied Python code.

### Thermal interface material resistance

\[
R_{TIM}=\frac{t_{TIM}}{k_{TIM}\times A_{die}}
\]

### Convective resistance

\[
R_{conv}=\frac{1}{h \times A_{total}}
\]

### Total thermal resistance

The supplied Python script calculates:

\[
R_{hs,script}=R_{conv}+R_{TIM}
\]

It then calculates:

\[
R_{total}=R_{jc}+R_{conv}+R_{TIM}
\]

Here, \(R_{jc}\) is the junction-to-case resistance.

**Implementation note:** The original script does not calculate base conduction resistance. The `r_conduction_c_per_w` output column is retained as 0.0 for output-schema compatibility. This is a placeholder and must not be interpreted as a physically calculated zero resistance.

### Junction temperature

\[
T_{junction}=T_{ambient}+TDP \times R_{total}
\]

## 5. Machine-Learning Implementation

Three input features were used:

- `tdp_w`
- `air_velocity_m_s`
- `k_tim_w_mk`

Two targets were predicted independently:

- `r_total_c_per_w`
- `junction_temperature_c`

### Random Forest Regressor

Random Forest is an ensemble learning algorithm that combines predictions from multiple decision trees. It can model nonlinear relationships between thermal input parameters and output values.

Configuration:

- Number of estimators: 200
- Maximum depth: 12
- Random state: 42

### Gradient Boosting Regressor

Gradient Boosting builds decision trees sequentially, with each new tree attempting to improve the prediction errors of the previous ensemble.

Configuration:

- Number of estimators: 150
- Learning rate: 0.05
- Maximum depth: 3
- Random state: 42

### Training and testing

The dataset was split into:

- 80% training data
- 20% testing data

The random state was set to 42 to make the split reproducible.

Both algorithms were trained separately for each target, resulting in four trained regression models.

## 6. Model Evaluation

The models were evaluated using three regression metrics.

- **MAE (Mean Absolute Error):** Measures the average absolute difference between predicted and actual values.
- **RMSE (Root Mean Squared Error):** Measures prediction error while giving greater weight to larger errors.
- **R² (Coefficient of Determination):** Measures how well the model explains the variation in the target values.

### Evaluation results

| Prediction target | Model | MAE | RMSE | R² |
|---|---|---:|---:|---:|
| Total resistance | Random Forest | 0.00000303 | 0.00001191 | 0.99999989 |
| Total resistance | Gradient Boosting | 0.00019652 | 0.00026358 | 0.99994378 |
| Junction temperature | Random Forest | 0.24825017 | 0.59519512 | 0.99930828 |
| Junction temperature | Gradient Boosting | 0.26615214 | 0.35698529 | 0.99975116 |

### Model comparison

For total thermal resistance, Random Forest achieved the lowest MAE and RMSE and the highest R².

For junction temperature, Gradient Boosting achieved the lowest RMSE and the highest R², while Random Forest achieved a slightly lower MAE.

Therefore:

- Random Forest is selected for total thermal resistance prediction.
- Gradient Boosting is selected for junction temperature prediction when RMSE and R² are the primary selection criteria.

Both algorithms performed well on the held-out test set from the generated simulation dataset.

These metrics measure agreement with the implemented simulation model. They do not independently establish accuracy against real heat-sink hardware or experimental measurements.

## 7. Feature Importance

Feature importance was obtained from the Random Forest and Gradient Boosting tree-based models.

The following tables show Random Forest feature importance.

### Total thermal resistance

| Feature | Random Forest importance |
|---|---:|
| TDP | 0.000002 |
| Air velocity | 0.927756 |
| TIM conductivity | 0.072242 |

Air velocity is the dominant feature for total thermal resistance in this simulation.

TDP has almost no importance because the implemented resistance calculation does not directly depend on TDP.

### Junction temperature

| Feature | Random Forest importance |
|---|---:|
| TDP | 0.923431 |
| Air velocity | 0.071383 |
| TIM conductivity | 0.005185 |

TDP is the dominant feature for junction temperature.

These findings are consistent with the implemented equations: TDP directly affects junction temperature through the heat-load term but does not directly affect the calculated thermal resistance.

Feature importance describes the model's use of input variables and should not be interpreted as an independent measurement of physical causality.

## 8. Correlation Analysis

Pearson correlation was used to study linear relationships between input parameters and thermal outputs.

| Input parameter | Total resistance correlation | Junction temperature correlation |
|---|---:|---:|
| TDP | 0.0000 | 0.9619 |
| Air velocity | -0.7982 | -0.1956 |
| TIM conductivity | -0.2127 | -0.0521 |

### Observations

1. TDP has a strong positive correlation with junction temperature.
2. Air velocity has a strong negative correlation with total thermal resistance.
3. TIM conductivity has a negative correlation with total thermal resistance.
4. TDP has approximately zero correlation with total resistance because the implemented resistance calculation is independent of TDP.

Correlation indicates association within the generated dataset and does not independently establish causation.

## 9. Sensitivity Analysis

One-factor sensitivity analysis was performed by grouping the dataset by each input parameter and calculating the average output.

| Input parameter | Output | Minimum average | Maximum average | Absolute change |
|---|---|---:|---:|---:|
| TDP | Total resistance | 0.312489 | 0.312489 | 0.000000 |
| TDP | Junction temperature | 34.374676 | 103.122302 | 68.747626 |
| Air velocity | Total resistance | 0.275265 | 0.410798 | 0.135534 |
| Air velocity | Junction temperature | 63.537032 | 82.511780 | 18.974748 |
| TIM conductivity | Total resistance | 0.305070 | 0.343871 | 0.038801 |
| TIM conductivity | Junction temperature | 67.709867 | 73.141965 | 5.432099 |

### Interpretation

- TDP has the largest effect on junction temperature.
- Air velocity has the largest effect on total thermal resistance.
- TIM conductivity also influences thermal performance, but its observed average effect is smaller.

Increasing air velocity reduces average total thermal resistance in the generated dataset.

Increasing TIM conductivity reduces average total thermal resistance and junction temperature.

Changing TDP affects junction temperature but does not change the calculated thermal resistance.

These changes represent averages across the other parameter combinations in the dataset, not isolated experimental measurements.

## 10. Reference Comparison and Limitations

The supplied reference report lists:

- Total heat-sink thermal resistance: 0.373043°C/W
- Junction temperature: 80.95652°C

At the baseline inputs of 150 W, 1 m/s air velocity, and 4 W/m·K TIM conductivity, the implemented calculation produced:

| Parameter | Implemented result |
|---|---:|
| Junction-to-case resistance | 0.200000°C/W |
| TIM resistance | 0.010582°C/W |
| Convective resistance | 0.158623°C/W |
| Script-defined `R_hs` aggregate | 0.169205°C/W |
| Total resistance | 0.369205°C/W |
| Junction temperature | 80.380740°C |

The implementation does not reproduce the reference values exactly.

The differences arise from inconsistencies and incomplete details in the supplied materials:

1. The reference report specifies junction-to-case resistance of 0.1°C/W, while the original supplied Python script uses 0.2°C/W.
2. The reference report includes base conduction resistance, whereas the original Python script does not calculate it.
3. The reference report separates TIM resistance from heat-sink resistance, whereas the original Python script combines TIM and convection resistance in its `R_hs` variable.
4. The supplied reference does not fully specify the total convection-area calculation.
5. The characteristic-length details in the convection calculation are not completely clear in the reference material.

The reference junction temperature also appears to use the reported heat-sink resistance directly in its temperature calculation, rather than the full resistance calculation implemented in the supplied Python script.

These differences have not been silently adjusted to force a numerical match. The implementation follows the original supplied Python script, and the discrepancies are documented transparently.

### Other limitations

1. The dataset is generated from mathematical thermal calculations rather than experimental hardware measurements.
2. Fin efficiency is not modelled.
3. Thermal radiation is not modelled.
4. Base conduction resistance is not included in the original supplied Python calculation.
5. Contact resistance beyond the specified junction-to-case and TIM terms is not included.
6. Model evaluation uses a random train-test split from the same simulation-generated parameter grid.
7. The results should not be treated as experimentally validated predictions.
8. Predictions outside the specified input ranges have not been validated.

## 11. Future Improvements

Potential improvements include:

- Validate the thermal equations against the original reference calculation and experimental measurements.
- Include fin efficiency and thermal radiation effects.
- Investigate alternative convection correlations and flow regimes.
- Evaluate models on parameter combinations excluded from training.
- Perform uncertainty and error analysis.
- Add an interactive interface for entering thermal parameters and viewing predictions.
- Explore additional regression algorithms and hyperparameter optimization.
- Compare simulation-based predictions against real heat-sink test data.

## 12. Project Deliverables

| Deliverable | Location |
|---|---|
| Thermal calculation model | `src/thermal_model.py` |
| Dataset generator | `src/parameter_sweep.py` |
| ML training and evaluation | `src/train_models.py` |
| Sensitivity and correlation analysis | `src/sensitivity_analysis.py` |
| Main execution script | `main.py` |
| Generated dataset | `data/thermal_dataset.csv` |
| Trained ML models | `models/` |
| Model metrics | `outputs/model_metrics.csv` |
| Feature importance | `outputs/feature_importance.csv` |
| Correlation matrix | `outputs/correlation_matrix.csv` |
| Correlation heatmap | `outputs/correlation_heatmap.png` |
| Sensitivity summary | `outputs/sensitivity_summary.csv` |
| Sensitivity plots | `outputs/sensitivity_*.png` |
| Technical report | `reports/technical_report.md` |

## 13. Conclusion

This project demonstrates a complete simulation-based workflow for thermal performance prediction using machine learning.

A dataset of 1,872 operating combinations was generated, and four regression models were trained across two prediction targets. Their performance was evaluated using MAE, RMSE, and R². Correlation, feature importance, and sensitivity analyses were also performed.

The results show that Random Forest performed best for total thermal resistance prediction. For junction temperature, Gradient Boosting achieved the strongest RMSE and R² results, while Random Forest achieved a slightly lower MAE.

The analysis indicates that air velocity is the dominant input influencing total thermal resistance, while TDP is the dominant input influencing junction temperature.

The implementation provides a foundation for AI-assisted thermal engineering analysis. Further validation against experimental measurements, improvement of the thermal calculation methodology, and clarification of the reference calculation discrepancies are necessary before using the predictions for real engineering design decisions.
