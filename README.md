# AIIP5 - AIIP Technical Assessment Submission

## a. Applicant information.

Applicant Name: **Tan Hun Chong** \
Email Address: **hunchong_tan@mymail.sutd.edu.sg** (previously stated on the application form) \
Secondary Email Address: **tanhunchong01@gmail.com** (preferred due to strict school email quarantines)

## b. Overview of the submitted folder and the folder structure.

    .
    ├── .github                             # Contains scripts to execute the end-to-end machine learning pipeline using GitHub Actions
    ├── .gitignore              
    ├── src                                 # Contains python files constituting the end-to-end ML pipeline
    │   ├── models                          # Empty folder for ML pipeline to insert the best models  
    │   ├── config.yaml                     # Allows user to choose whether to run Task 2a or Task 2b or both tasks
    │   ├── data_load.py                    # Load data from database    
    │   ├── data_preprocess.py              # Clean and pre-process raw data for readability 
    │   ├── model_train_and_evaluate.py     # Train and evaluate selected models to obtain the best models for pipeline   
    │   └── main.py                         # Contains the other python files to be run in one shot  
    ├── eda.ipynb                           # Interactive notebook explaining the findings of Task 1 - Exploratory Data Analysis (EDA)
    ├── requirements.txt                    # Specifies the external libraries and their respective versions needed to run the project
    ├── run.sh                              # To run modules/classes/scripts mentioned in the project
    ├── run_modular.sh                      # run.sh but more modular (Allows user to choose which Task 2a or 2b they wish to execute)   
    └── README.md


## c. Instructions for executing the pipeline and modifying any parameters.

### Windows Users:
- Use **Windows Subsystem for Linux (WSL)**, **Git Bash**, or **Cygwin** to run the pipeline.

### Linux and MacOS Users:
- Open a terminal and follow the steps below.

### Running the Pipeline
To execute the pipeline, choose one of the following methods:

#### 1. Standard Execution
Run the pipeline with default settings:
```bash run.sh```

#### 2. Modular Execution (Recommended)
Run the pipeline with more flexibility:
```bash run_modular.sh```
This allows you to execute Task 2A (Regression), Task 2B (Classification), or Both.

### Additional Information
For additional modifications related to database and models tested, please go directly to the related python files to customise parameters before running the pipeline.

## d. Description of logical steps/flow of the pipeline.
The machine learning pipeline follows these steps:

### 1. Data Retrieval and Loading (```data_load.py```)
The dataset is retrieved from the provided URL and saved as data/calls.db.
The dataset is thenloaded from calls.db using SQLite.

### 2. Data Cleaning and Preprocessing (```data_preprocess.py```)
The raw data is then cleaned and preprocessed.
For instance, missing values are handled, duplicates are removed, and data types are converted to ensure standardisation.
Some of the columns are renamed and reindexed for better clarity too.

### 3. Model Training and Evaluating (```model_train_and_evaluate.py```)
A series of feature engineering take place, including the encoding of categorical features and the scaling of numeric features.

#### 3a. Regression Model
For the task of predicting temperature, a regression model is required.
The column Temperature is used as the target feature.
This dataset is split into training and testing sets.
A set of three regression models are then trained:
- Linear Regression
- Random Forest Regressor
- XGBoost Regressor

After hyperparameter tuning, the best model is selected based on R² score and RMSE.

#### 3b. Classification Model
For the task of categorising Plant Type-Stage, a classification model is required.
A new column Plant Type-Stage is created by combining Plant Type and Plant Stage.
This dataset is split into training and testing sets.
A set of three classification models are trained:
- Logistic Regression
- Random Forest Classifier
- Support Vector Machine (SVM)

The best model is selected based on accuracy, precision, recall, and F1-score.

### 4. Model Deployment and Prediction (main.py)
The best-performing models are saved in the ```models/``` directory.
During inference, the trained models are automatically loaded.
Predictions are made for new data points.

## e. Overview of key findings from the EDA conducted in Task 1 and the choices made in the pipeline based on these findings, particularly any feature engineering.

### Key Insights from the EDA:

#### General Findings:
- Some sensor readings had missing values, which were handled using mean and median imputation.
- Certain numerical features contained outliers, which were removed using the Interquartile Range (IQR) method.

#### Task 2A: Predicting Tempature Conditions
- Potassium is a decent predictor.
- Plant Type is a great predictor.
- Plant Stage is a great predictor.
- All these 3 predictors can be used while the rest can be excluded.

#### Task 2B: Categorising Plant Type-Stage
- All plant types need more Light, CO2, Nutrients (Nitrogen, Phosphorus, Potassium) as it progresses from seedling to vegetative but does not need more when going from vegetative to maturity.
- More EC is produced as all plant types progress.
- All plant types need more water as it progresses from seedling to vegetative and to maturity.
- All plant types increase pH as it progresses from seedling to vegetative but does not increase when going from vegetative to maturity.

### Choices Made:
- Humidity Sensor data was dropped due to the high percentage of null values.
- There were a few negative values in the dataset, which were dropped because sensor data cannot logically be negative.
- Categorical features such as Plant Type and Plant Stage were transformed using one-hot encoding.
- Numeric features needed to undergo standardised scaling to make the models converge better.

## f. Describe how the features in the dataset are processed (summarised in a table).

*All numeric features also undergo Outlier Removal and Data Type Conversion to numeric.*

#### Task 2A: Predicting Tempature Conditions
Target Feature: ```Temperature Sensor (°C)```

| Feature Name                  | Data Type   | Processing Applied                         | Feature Engineering                        |
|--------------------------------|------------|--------------------------------------------|--------------------------------------------|
| System Location Code           | Categorical | -                                         | One-Hot Encoding                          |
| Previous Cycle Plant Type      | Categorical | Convert to lowercase                      | One-Hot Encoding                          |
| Plant Type                     | Categorical | Convert to lowercase                      | One-Hot Encoding                          |
| Plant Stage                    | Categorical | Convert to lowercase                      | One-Hot Encoding                          |
| Temperature Sensor (°C)        | Numerical   | Drop Negative Values                      | Standard Scaling                          |
| **Humidity Sensor (%)**        | Numerical   | **Dropped due to a high percentage of null values** | -                               |
| Light Intensity Sensor (lux)   | Numerical   | Median Imputation, Drop Negative Values   | Standard Scaling                          |
| CO2 Sensor (ppm)               | Numerical   | -                                         | Standard Scaling                          |
| O2 Sensor (ppm)                | Numerical   | -                                         | Standard Scaling                          |
| EC Sensor (dS/m)               | Numerical   | Drop Negative Values                      | Standard Scaling                          |
| Nutrient N Sensor (ppm)        | Numerical   | Mean Imputation                           | Standard Scaling                          |
| Nutrient P Sensor (ppm)        | Numerical   | Mean Imputation                           | Standard Scaling                          |
| Nutrient K Sensor (ppm)        | Numerical   | Median Imputation                         | Standard Scaling                          |
| Water Level Sensor (mm)        | Numerical   | Mean Imputation                           | Standard Scaling                          |
| pH Sensor                      | Numerical   | -                                         | Standard Scaling                          |

#### Task 2B: Categorising Plant Type-Stage
*As the task only states categorisation based on sensor data (numeric features), all categorical features are ignored.*
*A new column ['Plant Type-Stage'] is created by combining ['Plant Type'] + '-' + ['Plant Stage'].*
Target Feature: ```Plant Type-Stage```

| Feature Name                  | Data Type   | Processing Applied                         | Feature Engineering                        |
|--------------------------------|------------|--------------------------------------------|--------------------------------------------|
| Temperature Sensor (°C)        | Numerical   | Drop Negative Values                      | Standard Scaling                          |
| **Humidity Sensor (%)**        | Numerical   | **Dropped due to a high percentage of null values** | -                               |
| Light Intensity Sensor (lux)   | Numerical   | Median Imputation, Drop Negative Values   | Standard Scaling                          |
| CO2 Sensor (ppm)               | Numerical   | -                                         | Standard Scaling                          |
| O2 Sensor (ppm)                | Numerical   | -                                         | Standard Scaling                          |
| EC Sensor (dS/m)               | Numerical   | Drop Negative Values                      | Standard Scaling                          |
| Nutrient N Sensor (ppm)        | Numerical   | Mean Imputation                           | Standard Scaling                          |
| Nutrient P Sensor (ppm)        | Numerical   | Mean Imputation                           | Standard Scaling                          |
| Nutrient K Sensor (ppm)        | Numerical   | Median Imputation                         | Standard Scaling                          |
| Water Level Sensor (mm)        | Numerical   | Mean Imputation                           | Standard Scaling                          |
| pH Sensor                      | Numerical   | -                                         | Standard Scaling                          |

## g. Explanation of your choice of models for each machine learning task.


## h. Evaluation of the models developed. Any metrics used in the evaluation should also be explained.

## i. Other considerations for deploying the models developed.
