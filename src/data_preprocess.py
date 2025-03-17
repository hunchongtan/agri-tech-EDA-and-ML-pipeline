import pandas as pd
import numpy as np

'''
Cleaning Data Functions (as per eda.ipynb)
'''

# Separate relevant columns for cleaning
object_cols = [
    'System Location Code',
    'Previous Cycle Plant Type',
    'Plant Type',
    'Plant Stage'
]

numeric_cols = [
    'Temperature Sensor (°C)',
    'Humidity Sensor (%)',
    'Light Intensity Sensor (lux)',
    'CO2 Sensor (ppm)',
    'EC Sensor (dS/m)',
    'O2 Sensor (ppm)',
    'Nutrient N Sensor (ppm)',
    'Nutrient P Sensor (ppm)',
    'Nutrient K Sensor (ppm)',
    'pH Sensor',
    'Water Level Sensor (mm)'
]

# Fill empty cells with NaN
def fill_empty_cells_with_nan(df):
    return df.fillna(np.nan)

# Convert object columns to lowercase
def convert_object_columns_to_lowercase(df):
    local_object_cols = [col for col in object_cols if col != 'System Location Code']
    for col in local_object_cols:
        if col in df.columns:
            df[col] = df[col].str.lower()
    return df

# Convert numeric columns to fully numeric values
def convert_numeric_columns_to_fully_numeric_values(df):
    for col in numeric_cols:
        df[col] = df[col].astype(str)
        df[col] = df[col].str.replace(r'[^\d\.\-]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# Remove duplicates
def remove_duplicates(df):
    return df.drop_duplicates()

'''
Pre-processing Data Functions (as per eda.ipynb)
'''

# Remove rows with negative values in numeric columns
def remove_rows_with_negative_values_in_numeric_columns(df, numeric_cols):
    return df[~df[numeric_cols].lt(0).any(axis=1)]

# Drop humidity sensor column
def drop_humidity_sensor(df):
    return df.drop(columns=['Humidity Sensor (%)'])

# Impute missing values
def impute_missing_values(df): 
    df = df.copy()  # Avoid warnings

    # Mean imputation for selected columns
    mean_impute_cols = [
        'Temperature Sensor (°C)',
        'Nutrient N Sensor (ppm)',
        'Nutrient P Sensor (ppm)',
        'Water Level Sensor (mm)'
    ]
    for col in mean_impute_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())

    # Median imputation for selected columns
    median_impute_cols = [
        'Light Intensity Sensor (lux)',
        'Nutrient K Sensor (ppm)',
    ]
    for col in median_impute_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    return df

# Remove outliers in numeric columns using the IQR method
def remove_outliers(df, numeric_cols):
    for col in numeric_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df

# Rename and order columns for clarity
def rename_and_reorder_columns(df):
    rename_mapping = {
        'Previous Cycle Plant Type': 'Previous Plant Type',
        'Temperature Sensor (°C)': 'Temperature (°C)',
        'Light Intensity Sensor (lux)': 'Light Intensity (lux)',
        'CO2 Sensor (ppm)': 'CO2 (ppm)',
        'EC Sensor (dS/m)': 'EC (dS/m)',
        'O2 Sensor (ppm)': 'O2 (ppm)',
        'Nutrient N Sensor (ppm)': 'Nitrogen (ppm)',
        'Nutrient P Sensor (ppm)': 'Phosphorus (ppm)',
        'Nutrient K Sensor (ppm)': 'Potassium (ppm)',
        'pH Sensor': 'pH',
        'Water Level Sensor (mm)': 'Water Level (mm)'
    }
    df = df.rename(columns=rename_mapping)
    new_order = [
        'System Location Code',
        'Plant Type',
        'Plant Stage',
        'Previous Plant Type',
        'Temperature (°C)',
        'Light Intensity (lux)',
        'CO2 (ppm)',
        'O2 (ppm)',
        'EC (dS/m)',
        'Nitrogen (ppm)',
        'Phosphorus (ppm)',
        'Potassium (ppm)',
        'Water Level (mm)',
        'pH'
    ]
    df = df.reindex(columns=new_order)
    df = df.sort_values(by=['System Location Code', 'Plant Type', 'Plant Stage', 'Previous Plant Type']).reset_index(drop=True)
    return df

'''
MAIN Clean and Preprocess Data Function
'''

def clean_data(df):
    df = fill_empty_cells_with_nan(df)
    df = convert_object_columns_to_lowercase(df)
    df = convert_numeric_columns_to_fully_numeric_values(df)
    df = remove_duplicates(df)

    return df

def preprocess_data(df):
    df = remove_rows_with_negative_values_in_numeric_columns(df, numeric_cols)
    df = drop_humidity_sensor(df)
    df = impute_missing_values(df)
    df = remove_outliers(df, numeric_cols)
    df = rename_and_reorder_columns(df)
    return df

def data_preprocess(df):
    df = clean_data(df)   
    df = preprocess_data(df)

    print("Data preprocessed successfully.")
    return df


if __name__ == "__main__":
    from data_load import data_load
    df = data_load()
    df = data_preprocess(df)
    print("Preview Dataset:")
    print(df.head())
    print("-" * 50)
    print("Dataset Info:")
    print(df.info())