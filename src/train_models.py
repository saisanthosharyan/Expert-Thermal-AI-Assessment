
"""
Train and evaluate machine-learning models for thermal prediction.

Models:
1. Random Forest Regressor
2. Gradient Boosting Regressor

Targets:
- Total thermal resistance
- Junction temperature
"""

import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


DATASET_PATH = "data/thermal_dataset.csv"
MODEL_DIR = "models"
OUTPUT_DIR = "outputs"

FEATURES = [
    "tdp_w",
    "air_velocity_m_s",
    "k_tim_w_mk",
]

TARGETS = [
    "r_total_c_per_w",
    "junction_temperature_c",
]


def train_and_evaluate():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load dataset
    data = pd.read_csv(DATASET_PATH)

    X = data[FEATURES]
    X_train, X_test, y_train_all, y_test_all = train_test_split(
        X,
        data[TARGETS],
        test_size=0.20,
        random_state=42
    )

    # Define two ML algorithms
    model_types = {
        "random_forest": RandomForestRegressor(
            n_estimators=200,
            max_depth=12,
            random_state=42,
            n_jobs=-1
        ),
        "gradient_boosting": GradientBoostingRegressor(
            n_estimators=150,
            learning_rate=0.05,
            max_depth=3,
            random_state=42
        ),
    }

    results = []
    feature_importance_results = []

    # Train one model per algorithm and prediction target
    for target in TARGETS:
        y_train = y_train_all[target]
        y_test = y_test_all[target]

        print(f"\n{'=' * 55}")
        print(f"TARGET: {target}")
        print(f"{'=' * 55}")

        for model_name, model_template in model_types.items():
            # Create an independent model for this target
            model = model_template.__class__(
                **model_template.get_params()
            )

            model.fit(X_train, y_train)
            predictions = model.predict(X_test)

            mae = mean_absolute_error(y_test, predictions)
            rmse = np.sqrt(mean_squared_error(y_test, predictions))
            r2 = r2_score(y_test, predictions)

            results.append({
                "model": model_name,
                "target": target,
                "MAE": mae,
                "RMSE": rmse,
                "R2": r2,
            })

            # Save trained model
            model_filename = f"{model_name}_{target}.joblib"
            model_path = os.path.join(MODEL_DIR, model_filename)
            joblib.dump(model, model_path)

            print(f"\nModel: {model_name}")
            print(f"MAE : {mae:.8f}")
            print(f"RMSE: {rmse:.8f}")
            print(f"R2  : {r2:.8f}")
            print(f"Saved: {model_path}")

            # Record feature importance
            if hasattr(model, "feature_importances_"):
                for feature, importance in zip(
                    FEATURES, model.feature_importances_
                ):
                    feature_importance_results.append({
                        "model": model_name,
                        "target": target,
                        "feature": feature,
                        "importance": importance,
                    })

    # Save evaluation metrics
    results_df = pd.DataFrame(results)
    metrics_path = os.path.join(OUTPUT_DIR, "model_metrics.csv")
    results_df.to_csv(metrics_path, index=False)

    # Save feature importance
    importance_df = pd.DataFrame(feature_importance_results)
    importance_path = os.path.join(
        OUTPUT_DIR, "feature_importance.csv"
    )
    importance_df.to_csv(importance_path, index=False)

    print(f"\n{'=' * 55}")
    print("MODEL COMPARISON")
    print(f"{'=' * 55}")
    print(results_df.to_string(index=False))

    print("\nFeature importance:")
    print(importance_df.to_string(index=False))

    print(f"\nMetrics saved to: {metrics_path}")
    print(f"Feature importance saved to: {importance_path}")
    print("\nAll four models trained and saved successfully!")


if __name__ == "__main__":
    train_and_evaluate()
