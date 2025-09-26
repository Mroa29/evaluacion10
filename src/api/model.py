# -*- coding: utf-8 -*-
"""
Model loader and prediction utilities.

Key behaviors:
- Reads MODEL_PATH dynamically on each access (env var), defaulting to "model.pkl".
- Caches the loaded model but will reload it if the path changes (e.g., tests monkeypatch or retraining).
- Provides predict_batch() for dict inputs (Age, EstimatedSalary) and array-like inputs.
"""

import os
import joblib
import numpy as np

# Cached model and the path it was loaded from
_model = None
_model_loaded_from = None


def _get_model_path() -> str:
    """Return the current model path, resolved from environment each time."""
    return os.getenv("MODEL_PATH", "model.pkl")


def get_model():
    """Load (or reload) the model from disk if needed and return it.
    - Loads if cache is empty, or if MODEL_PATH has changed since the last load.
    - Raises FileNotFoundError if the path does not exist.
    """
    global _model, _model_loaded_from
    path = _get_model_path()

    if _model is None or _model_loaded_from != path:
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Model file not found at {path}. Set MODEL_PATH env var or place model.pkl alongside app."
            )
        _model = joblib.load(path)
        _model_loaded_from = path
    return _model


def predict_batch(rows, feature_order=None):
    """Predict for a batch of rows.

    Args:
        rows: list of dicts with keys ["Age","EstimatedSalary"], or list/array of pairs.
        feature_order: explicit key order for dict inputs; defaults to ["Age","EstimatedSalary"].

    Returns:
        list of {"prediction": int, "proba": float|None}
    """
    if not rows:
        return []

    if isinstance(rows[0], dict):
        feature_order = feature_order or ["Age", "EstimatedSalary"]
        X = np.array([[float(r[k]) for k in feature_order] for r in rows], dtype=float)
    else:
        X = np.array(rows, dtype=float)

    model = get_model()

    proba = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)[:, -1].tolist()
    elif hasattr(model, "decision_function"):
        import math
        df = model.decision_function(X)
        proba = [1 / (1 + math.exp(-z)) for z in np.ravel(df)]

    preds = model.predict(X).tolist()
    return [
        {"prediction": int(p), "proba": (float(proba[i]) if proba is not None else None)}
        for i, p in enumerate(preds)
    ]
