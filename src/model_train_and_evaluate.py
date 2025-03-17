import joblib
import yaml
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
from sklearn.svm import SVR, SVC
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score

# Load configuration file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

TASK = config["task"]  # Edit to "regression" (Task 2a), "classification" (Task 2b), or "both"

# All available regression and classification models (with hyperparameters)
models = {
    "regression": {
        "Linear Regression": {
            "model": LinearRegression(),
            "params": {}
        },
        "Random Forest": {
            "model": RandomForestRegressor(random_state=42),
            "params": {"n_estimators": [100, 200], "max_depth": [None, 5, 10]}
        },
        "XGBoost": {
            "model": XGBRegressor(objective="reg:squarederror", random_state=42),
            "params": {"n_estimators": [100, 200], "max_depth": [3, 5, 7]}
        },
    },
    "classification": {
        "Logistic Regression": {
            "model": LogisticRegression(max_iter=1000),
            "params": {}
        },
        "Random Forest": {
            "model": RandomForestClassifier(random_state=42),
            "params": {"n_estimators": [100, 200], "max_depth": [None, 5, 10]}
        },
        "SVM": {
            "model": SVC(),
            "params": {"C": [0.1, 1, 10], "kernel": ["linear", "rbf"]}
        }
    }
}

# Create Plant Type-Stage column for Task 2b
def create_plant_type_stage(df):
    df['Plant Type-Stage'] = df['Plant Type'] + '-' + df['Plant Stage']
    return df

# Split dataset into training and testing sets (80% training, 20% testing)
def train_test_split_data(df, target_col):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return train_test_split(X, y, test_size=0.2, random_state=42)

# Evaluate regression models using R² and RMSE
def evaluate_regression_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    return r2, rmse

# Evaluate classification models using Accuracy, Precision, Recall, and F1-score
def evaluate_classification_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")
    return accuracy, precision, recall, f1

# Trains a given model and evaluates it
def train_and_evaluate_model(model_name, model_dict, X_train, y_train, X_test, y_test, task_type):
    model = model_dict["model"]
    param_grid = model_dict["params"]

    print(f"Training {model_name} with GridSearchCV!")

    grid_search = GridSearchCV(model, param_grid, cv=3, scoring="accuracy" if task_type == "classification" else "r2", n_jobs=-1)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    print(f"{model_name} Best Params: {grid_search.best_params_}")

    if task_type == "regression":
        r2, rmse = evaluate_regression_model(best_model, X_test, y_test)
        print(f"{model_name}: R² = {r2:.3f}, RMSE = {rmse:.3f}")
        print("-" * 5)
        return best_model, r2, grid_search.best_params_

    elif task_type == "classification":
        accuracy, precision, recall, f1 = evaluate_classification_model(best_model, X_test, y_test)
        print(f"{model_name}: Accuracy = {accuracy:.3f}, Precision = {precision:.3f}, Recall = {recall:.3f}, F1-Score = {f1:.3f}")
        print("-" * 5)
        return best_model, accuracy, grid_search.best_params_

# Finds the best model based on R² (regression) or Accuracy (classification)
def find_best_model(models, X_train, y_train, X_test, y_test, task_type):
    best_model = None
    best_score = float("-inf")
    best_model_name = ""
    best_params = None

    for model_name, model_dict in models.items():
        model, score, params = train_and_evaluate_model(model_name, model_dict, X_train, y_train, X_test, y_test, task_type)

        if score > best_score:
            best_score = score
            best_model = model
            best_model_name = model_name
            best_params = params

    print(f"Best {task_type} model: {best_model_name} ({best_params}) with score: {best_score:.3f}")
    return best_model, best_model_name

def model_train_and_evaluate(df):
    run_regression = TASK in ["regression", "both"]
    run_classification = TASK in ["classification", "both"]

    # Run regression task
    if run_regression:
        print("-" * 50)
        print("Running Regression Models...")
        print("-" * 5)

        target_col = 'Temperature (°C)'

        df_reg = df.copy()

        # Encode categorical features
        categorical_features = df_reg.select_dtypes(include=['object', 'category']).columns
        df_reg = pd.get_dummies(df_reg, columns=categorical_features, drop_first=True)

        X_train, X_test, y_train, y_test = train_test_split_data(df_reg, target_col)
        
        best_model, best_model_name = find_best_model(models["regression"], X_train, y_train, X_test, y_test, "regression")
        joblib.dump(best_model, f"models/{best_model_name}_regression.pkl")

    # Run classification task
    if run_classification:
        print("-" * 50)
        print("Running Classification Models...")
        print("-" * 5)
        
        target_col = 'Plant Type-Stage'
        
        df_clf = df.copy()
        df_clf = create_plant_type_stage(df_clf)

        sensor_data = list(df.select_dtypes(include=['float64', 'int64']).columns)

        df_clf = df_clf[sensor_data + [target_col]]
        
        X_train, X_test, y_train, y_test = train_test_split_data(df_clf, target_col)
        
        # Scale numeric features to help models converge
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        
        best_model, best_model_name = find_best_model(models["classification"], X_train, y_train, X_test, y_test, "classification")
        joblib.dump(best_model, f"models/{best_model_name}_classification.pkl")

if __name__ == "__main__":
    from data_load import data_load
    from data_preprocess import data_preprocess

    df = data_load()
    df = data_preprocess(df)

    model_train_and_evaluate(df)

    print("-" * 50)
    print("All available models trained and evaluated!")
