import joblib
import yaml
import os
import glob
import pandas as pd
from data_load import data_load
from data_preprocess import data_preprocess
from model_train_and_evaluate import model_train_and_evaluate, create_plant_type_stage

# Load configuration file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

TASK = config["task"]

# Load the best model from the models directory
def load_best_model(task_type):
    model_files = glob.glob(f"models/*_{task_type}.pkl")

    if not model_files:
        print(f"No trained {task_type} model found.")
        return None

    best_model_file = max(model_files, key=os.path.getctime)

    return joblib.load(best_model_file)

if __name__ == "__main__":
    print("Running Machine Learning Pipeline...")

    # Load and preprocess data
    df = data_load()
    df = data_preprocess(df)

    # Train and evaluate models
    model_train_and_evaluate(df)
    print("-" * 50)

    # Load the best models
    best_regression_model = load_best_model("regression") if TASK in ["regression", "both"] else None
    best_classification_model = load_best_model("classification") if TASK in ["classification", "both"] else None

    # Predicting temperature (Regression)
    if best_regression_model:
        print("\nUsing Regression Model:", best_regression_model)
        target_col = "Temperature (°C)"
        sample_features = df.drop(columns=[target_col]).iloc[0:1]

        # Apply one-hot encoding to match training data
        sample_features = pd.get_dummies(sample_features, drop_first=True)

        # Ensure the sample has the same features as the trained model
        missing_cols = set(best_regression_model.feature_names_in_) - set(sample_features.columns)
        for col in missing_cols:
            sample_features[col] = 0
        sample_features = sample_features[best_regression_model.feature_names_in_]

        # Predict Temperature
        temperature_prediction = best_regression_model.predict(sample_features)
        print(f"🎯 Predicted Temperature: {temperature_prediction[0]:.2f}°C")

    # Categorising Plant Type-Stage (Classification)
    if best_classification_model:
        print("\nUsing Classification Model:", best_classification_model)

        df = create_plant_type_stage(df)
        sensor_data = list(df.select_dtypes(include=['float64', 'int64']).columns)

        target_col = "Plant Type-Stage"
        df = df[sensor_data + [target_col]]

        sample_features = df.drop(columns=[target_col]).iloc[0:1]

        # Predict Plant Type-Stage
        plant_stage_prediction = best_classification_model.predict(sample_features.values)
        print(f"🎯 Predicted Plant Type-Stage: {plant_stage_prediction[0]}")

    print("-" * 50)
    print("Machine Learning Pipeline Completed!")
