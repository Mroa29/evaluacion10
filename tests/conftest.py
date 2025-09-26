# -*- coding: utf-8 -*-
"""Pytest configuration and fixtures for the API tests."""
import os
import sys
import tempfile
import joblib
import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression

# Ensure project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.main import create_app  # noqa: E402

@pytest.fixture
def temp_model_path(tmp_path):
    """Create and return a temporary sklearn model file (model.pkl)."""
    X = np.array([[20, 20000], [35, 45000], [52, 120000], [41, 80000]], dtype=float)
    y = np.array([0, 0, 1, 1], dtype=int)
    clf = LogisticRegression()
    clf.fit(X, y)

    model_file = tmp_path / "model.pkl"
    joblib.dump(clf, model_file)
    return str(model_file)

@pytest.fixture
def client(temp_model_path):
    """Flask test client with MODEL_PATH pointing to the temporary model."""
    os.environ["MODEL_PATH"] = temp_model_path
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()
