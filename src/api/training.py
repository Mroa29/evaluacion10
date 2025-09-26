# -*- coding: utf-8 -*-
"""
Training helpers for the Flask API.

Supports:
- Training from a CSV file with columns ["Age","EstimatedSalary"] (like the original class notebook).
- Training from JSON data (list of dicts with those keys).
- Synthetic fallback if no data is provided.
Saves the model to MODEL_PATH (defaults to "model.pkl").
"""
import os
import io
import json
import joblib
import numpy as np

MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")

def _fit_and_save(X, y):
    from sklearn.linear_model import LogisticRegression
    clf = LogisticRegression()
    clf.fit(X, y)
    joblib.dump(clf, MODEL_PATH)
    return clf

def train_from_json(instances):
    # instances: list of dicts: {"Age": .., "EstimatedSalary": .., "label": 0/1}
    if not instances:
        raise ValueError("No instances provided")
    X, y = [], []
    for row in instances:
        X.append([float(row["Age"]), float(row["EstimatedSalary"])])
        y.append(int(row["label"]))
    X = np.array(X, dtype=float)
    y = np.array(y, dtype=int)
    clf = _fit_and_save(X, y)
    return {"samples": len(y), "coef_": getattr(clf, "coef_", None).tolist(), "classes_": clf.classes_.tolist()}

def train_from_csv(csv_path):
    import pandas as pd
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found at {csv_path}")
    df = pd.read_csv(csv_path)
    # Heuristics for column names used in the course
    feature_cols = ["Age", "EstimatedSalary"]
    target_col = None
    # Try common target names
    for cand in ["Purchased", "label", "target", "y"]:
        if cand in df.columns:
            target_col = cand
            break
    if target_col is None:
        raise ValueError("Target column not found (tried: Purchased, label, target, y)")
    X = df[feature_cols].astype(float).values
    y = df[target_col].astype(int).values
    clf = _fit_and_save(X, y)
    return {"samples": int(len(y)), "coef_": getattr(clf, "coef_", None).tolist(), "classes_": clf.classes_.tolist()}

def train_synthetic(n_samples=300, seed=42):
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=n_samples, n_features=2, n_informative=2, n_redundant=0, random_state=seed)
    clf = _fit_and_save(X, y)
    return {"samples": int(n_samples), "coef_": getattr(clf, "coef_", None).tolist(), "classes_": clf.classes_.tolist()}
