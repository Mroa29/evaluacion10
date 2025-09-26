# -*- coding: utf-8 -*-
def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json().get("status") == "ok"

def test_predict_single_instance(client):
    payload = {"instances": [{"Age": 35, "EstimatedSalary": 45000}]}
    resp = client.post("/api/predict", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert "results" in data and isinstance(data["results"], list) and len(data["results"]) == 1
    item = data["results"][0]
    assert "prediction" in item
    # proba can be None if model lacks predict_proba, but for LogisticRegression it should exist
    assert "proba" in item and item["proba"] is not None
