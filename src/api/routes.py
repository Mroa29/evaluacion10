# -*- coding: utf-8 -*-
"""
API routes (Blueprint)
/api/health        -> GET
/api/predict       -> POST JSON: {"instances":[{"Age": 35, "EstimatedSalary": 45000}, ...]}
"""
from flask import Blueprint, jsonify, request
from .model import predict_batch

api_bp = Blueprint("api", __name__)

@api_bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@api_bp.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    instances = payload.get("instances") or payload.get("data")
    if instances is None:
        return jsonify({"error": "Missing 'instances' (list). Example: {'instances': [{'Age': 35, 'EstimatedSalary': 45000}] }"}), 400
    try:
        results = predict_batch(instances)
        return jsonify({"results": results}), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@api_bp.post("/train")
def train():
    """
    POST JSON options:
    - {"csv_path": "data/SocialNetworkAds.csv"}
    - {"instances": [{"Age": 35, "EstimatedSalary": 45000, "label": 0}, ...]}
    - {}  -> synthetic fallback
    """
    from .training import train_from_csv, train_from_json, train_synthetic
    payload = request.get_json(silent=True) or {}

    try:
        if "csv_path" in payload:
            info = train_from_csv(payload["csv_path"])
        elif isinstance(payload.get("instances"), list):
            info = train_from_json(payload["instances"])
        else:
            info = train_synthetic()
        return jsonify({"status": "trained", "details": info}), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400
