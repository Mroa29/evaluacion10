# -*- coding: utf-8 -*-
import os
import numpy as np
from src.api import model as model_mod

def test_predict_batch_with_dicts(monkeypatch, temp_model_path):
    # Point loader to temp model
    monkeypatch.setenv("MODEL_PATH", temp_model_path)
    # Reset cached model in module (in case of repeated runs)
    model_mod._model = None

    rows = [{"Age": 41, "EstimatedSalary": 80000},
            {"Age": 22, "EstimatedSalary": 18000}]
    out = model_mod.predict_batch(rows)
    assert isinstance(out, list) and len(out) == 2
    assert {"prediction", "proba"}.issubset(out[0].keys())

def test_predict_batch_with_arrays(monkeypatch, temp_model_path):
    monkeypatch.setenv("MODEL_PATH", temp_model_path)
    model_mod._model = None

    rows = np.array([[50.0, 120000.0], [30.0, 30000.0]])
    out = model_mod.predict_batch(rows.tolist())
    assert isinstance(out, list) and len(out) == 2
    assert "prediction" in out[0]
