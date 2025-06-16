import argparse
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# ---- Argument parsing ----
parser = argparse.ArgumentParser()
parser.add_argument("--input_data", type=str)
parser.add_argument("--output_dir", type=str)
args = parser.parse_args()

# country risk score dictionary ----
country_risk = {'Nigeria': 3, 'India': 2, 'Ghana': 2, 'Kenya': 2, 
                       'Germany': 0, 'USA': 0, 'UK': 0, 'Pakistan': 3, 
                       'South Africa': 1, 'Egypt': 2}

try:
    df = pd.read_csv(args.input_data)
    df.drop("risk_score", axis=1, inplace=True)

    df["country_risk_score"] = df["country"].map(country_risk)
    df.drop("country", axis=1, inplace=True)

    df["sponsorship"] = df["sponsorship"].map({"Yes": 1, "No": 0})

    label = df["risk_flag"].values  # (n_samples,) array

    # Drop label and encode the rest
    df = df.drop("risk_flag", axis=1)

    # Define features
    num_features = ['age', 'financial_support','travel_history', 'duration']
    cat_features = ['visa_type', 'employment_status', 'purpose']

    num_transformer = Pipeline([
        ("scaler", StandardScaler())
    ])

    cat_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

    preprocessor = ColumnTransformer([
        ("num", num_transformer, num_features),
        ("cat", cat_transformer, cat_features),
    ])

    preprocessed_data = preprocessor.fit_transform(df)

    # ---- Save outputs ----
    os.makedirs(args.output_dir, exist_ok=True)
    np.save(os.path.join(args.output_dir, "data.npy"), preprocessed_data)
    np.save(os.path.join(args.output_dir, "y.npy"), label)
    joblib.dump(preprocessor, os.path.join(args.output_dir, "preprocessor.pkl"))

    print("Preprocessing complete.")

except Exception as e:
    print("Error during preprocessing:", e)
    raise
