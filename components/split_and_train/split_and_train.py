import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_data", type=str, help="Path to preprocessed folder")
    parser.add_argument("--model_output", type=str, help="Path to save model")
    args = parser.parse_args()

    output_dir = args.input_data
    # Load preprocessed data

    X = np.load(os.path.join(args.input_data, "data.npy"))
    y = np.load(os.path.join(args.input_data, "y.npy"))


    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Validation Accuracy: {acc:.4f}")

    # Save model
    os.makedirs(args.model_output, exist_ok=True)
    joblib.dump(model, os.path.join(args.model_output, "model.pkl"))

if __name__ == "__main__":
    main()
