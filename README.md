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

### 4. Model Deployment and Prediction (```main.py```)
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
- Numeric features can undergo standardised scaling to make the models (especially classification models) converge better.

## f. Describe how the features in the dataset are processed (summarised in a table).

*All numeric features also undergo Outlier Removal and Data Type Conversion to numeric.*

#### Task 2A: Predicting Tempature Conditions
*Standardised scaling not done for numeric features since Random Forest Regressor and XGBoost generally do not need scaling.*

Target Feature: ```Temperature Sensor (°C)```

| Feature Name                  | Data Type   | Processing Applied                         | Feature Engineering                        |
|--------------------------------|------------|--------------------------------------------|--------------------------------------------|
| System Location Code           | Categorical | -                                         | One-Hot Encoding                          |
| Previous Cycle Plant Type      | Categorical | Convert to lowercase                      | One-Hot Encoding                          |
| Plant Type                     | Categorical | Convert to lowercase                      | One-Hot Encoding                          |
| Plant Stage                    | Categorical | Convert to lowercase                      | One-Hot Encoding                          |
| **Temperature Sensor (°C)**    | Numerical   | Drop Negative Values                      | -                                         |
| *Humidity Sensor (%)*          | Numerical   | **Dropped due to a high percentage of null values** | -                               |
| Light Intensity Sensor (lux)   | Numerical   | Median Imputation, Drop Negative Values   | -                                         |
| CO2 Sensor (ppm)               | Numerical   | -                                         | -                                         |
| O2 Sensor (ppm)                | Numerical   | -                                         | -                                         |
| EC Sensor (dS/m)               | Numerical   | Drop Negative Values                      | -                                         |
| Nutrient N Sensor (ppm)        | Numerical   | Mean Imputation                           | -                                         |
| Nutrient P Sensor (ppm)        | Numerical   | Mean Imputation                           | -                                         |
| Nutrient K Sensor (ppm)        | Numerical   | Median Imputation                         | -                                         |
| Water Level Sensor (mm)        | Numerical   | Mean Imputation                           | -                                         |
| pH Sensor                      | Numerical   | -                                         | -                                         |

#### Task 2B: Categorising Plant Type-Stage
*As the task only states categorisation based on sensor data (numeric features), all categorical features are ignored.*
*A new column ['Plant Type-Stage'] is created by combining ['Plant Type'] + '-' + ['Plant Stage'].*

Target Feature: ```Plant Type-Stage```

| Feature Name                  | Data Type   | Processing Applied                         | Feature Engineering                        |
|--------------------------------|------------|--------------------------------------------|--------------------------------------------|
| **Plant Type-Stage**           | Categorical | Combine 'Plant Type' + 'Plant Stage'      | -                                         |
| Temperature Sensor (°C)        | Numerical   | Drop Negative Values                      | Standard Scaling                          |
| *Humidity Sensor (%)*          | Numerical   | **Dropped due to a high percentage of null values** | -                               |
| Light Intensity Sensor (lux)   | Numerical   | Median Imputation, Drop Negative Values   | Standard Scaling                          |
| CO2 Sensor (ppm)               | Numerical   | -                                         | Standard Scaling                          |
| O2 Sensor (ppm)                | Numerical   | -                                         | Standard Scaling                          |
| EC Sensor (dS/m)               | Numerical   | Drop Negative Values                      | Standard Scaling                          |
| Nutrient N Sensor (ppm)        | Numerical   | Mean Imputation                           | Standard Scaling                          |
| Nutrient P Sensor (ppm)        | Numerical   | Mean Imputation                           | Standard Scaling                          |
| Nutrient K Sensor (ppm)        | Numerical   | Median Imputation                         | Standard Scaling                          |
| Water Level Sensor (mm)        | Numerical   | Mean Imputation                           | Standard Scaling                          |
| pH Sensor                      | Numerical   | -                                         | Standard Scaling                          |

*Sidenote: Without scaling, classification models were giving scores of 1.000. This is a sign of overfitting and potential data leakage. As such, standard scaling was implemented on numerical features.

## g. Explanation of your choice of models for each machine learning task.
The following models were selected for their effectiveness in each task:

#### Task 2A: Predicting Tempature Conditions (Regression Models)
Temperature prediction requires a regression model since the target variable is continuous.
The following 3 models were chosen:
##### 1. Linear Regression:
- Acts as a baseline model to assess performance against more complex models.
- Easy to intrepret
- Works well when the relationship between features and temperature is approximately linear.

##### 2. Random Forest Regressor
- Handles non-linear relationships better than Linear Regression.
- Uses multiple decision trees, reducing the impact of outliers and noisy data.
- Less prone to overfitting due to its ensemble approach.

##### 3. XGBoost Regressor
- High-performance boosting algorithm known for its predictive accuracy.
- Less prone to overfitting due to its built-in regularisation.
- Easy to undergo hyperparameter tuning for further fine-tuning.

#### Task 2B: Categorising Plant Type-Stage (Classification Models)
For categorising plant type-stage, a classification model was necessary.
The following 3 models were chosen:
##### 1. Logistic Regression
- Acts as a baseline model to assess performance against more complex models.
- Easy to intrepret
- Works well when the target categories are linearly separable.

##### 2. Random Forest Classifier
- Handles both categorical and numerical features effectively, reducing the need for extensive preprocessing.
- Uses multiple decision trees, reducing the impact of outliers and noisy data.
- Less prone to overfitting due to its ensemble approach.

##### 3. Support Vector Machine (SVM)
- Effective for classification problems with complex decision boundaries.
- Uses a kernel trick to transform data into higher-dimensional space, improving accuracy for non-linearly separable data.
- Provides high accuracy in well-defined classification tasks.

## h. Evaluation of the models developed. Any metrics used in the evaluation should also be explained.
All models (if applicable) undergo hyperparameter tuning using Grid Search to find the optimal parameters.

##### Hyperparameter Tuning with Grid Search
Grid Search systematically tests different hyperparameter combinations to identify the best-performing model. It evaluates multiple configurations based on a chosen metric (e.g., R² for regression or accuracy for classification) and selects the optimal parameters.

#### Task 2A: Predicting Tempature Conditions (Regression Models)
![image](https://github.com/user-attachments/assets/359e1ea9-b8d3-450d-bc31-2308603b1b1b)

##### Regression Evaluation Metrics:
- R² Score: Measures how well the model fits the data. A higher R² (closer to 1) indicates a better fit.
- Root Mean Squared Error (RMSE): Evaluates prediction error magnitude. A lower RMSE indicates more precise predictions.

We use the R² Score as the main evaluation metric since it directly indicates how well the model captures variations in temperature.

##### Winner: Random Forest Regressor ({'max_depth': 10, 'n_estimators': 200}) with R² Score: 0.565

#### Task 2B: Categorising Plant Type-Stage (Classification Models)
![image](https://github.com/user-attachments/assets/9785c398-6b52-433a-8538-c4d9d00125ed)

##### Classification Evaluation Metrics:
Accuracy: Percentage of correct classifications.
Precision: Percentage of relevant predictions among all positive predictions.
Recall: Ability of the model to find all relevant cases.
F1-Score: Harmonic mean of Precision and Recall.

We use Accuracy as the primary metric since it provides a clear overall measure of classification performance.

##### Winner: Random Forest Classifier ({'max_depth': None, 'n_estimators': 100}) with Accuracy: 0.769

#### Predictions
With these winning models, we can make our predictions! :)

![image](https://github.com/user-attachments/assets/2359d3c0-92aa-4877-ada4-a1cbe6eff1a1)

## i. Other considerations for deploying the models developed.
1. The pipeline is designed to handle large datasets efficiently with minimal modifications.
2. The entire workflow, from data preprocessing to model training and fine-tuning, is automated. Simply running bash run.sh can quickly retrain and evaluate models.
3. The config.yaml file allows users to modify tasks (regression, classification, or both) without changing the code. This ensures flexibility in running different experiments based on user needs.
4. From personal testing, the models train and evaluate quickly, making the pipeline suitable for rapid iteration.
5. Best models are also stored in the pipeline. If not necessary to retrain models, a simple comment on the model training code snippet in main.py can allow the same models to be used over and over again.
