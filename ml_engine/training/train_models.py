"""
Train dummy ML models and export them to the ml_models directory.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

try:
    from .datasets import load_datasets, split_features_labels
except ImportError:
    from datasets import load_datasets, split_features_labels


DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "ml_models"


def _train_risk_scoring(df: pd.DataFrame) -> Dict:
    features, labels = split_features_labels(df)
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels
    )
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    return {
        "model": model,
        "metrics": {
            "accuracy": float(accuracy_score(y_test, preds)),
            "f1": float(f1_score(y_test, preds)),
        },
    }


def _train_audio_classification(df: pd.DataFrame) -> Dict:
    features, labels = split_features_labels(df)
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(labels)
    X_train, X_test, y_train, y_test = train_test_split(
        features, y_encoded, test_size=0.2, random_state=7, stratify=y_encoded
    )
    model = RandomForestClassifier(n_estimators=120, random_state=7)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    return {
        "model": model,
        "label_encoder": encoder,
        "metrics": {
            "accuracy": float(accuracy_score(y_test, preds)),
            "f1": float(f1_score(y_test, preds, average="weighted")),
        },
    }


def _train_anomaly_detection(df: pd.DataFrame) -> Dict:
    features, labels = split_features_labels(df)
    model = IsolationForest(contamination=0.15, random_state=21)
    model.fit(features)

    preds = model.predict(features)
    preds = (preds == -1).astype(int)
    metrics = {}
    if labels is not None:
        metrics["accuracy"] = float(accuracy_score(labels, preds))
        metrics["f1"] = float(f1_score(labels, preds))

    return {
        "model": model,
        "metrics": metrics,
    }


def _write_artifact(payload: Dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, output_path)


def _write_metadata(metadata: Dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)


def train_all(data_dir: Path | None, output_dir: Path, use_existing_only: bool) -> Dict:
    datasets = load_datasets(data_dir=data_dir, use_existing_only=use_existing_only)

    results = {}

    risk_result = _train_risk_scoring(datasets["risk_scoring"])
    risk_path = output_dir / "risk_scoring_model.joblib"
    _write_artifact(risk_result, risk_path)
    results["risk_scoring"] = {
        "artifact": str(risk_path),
        "metrics": risk_result["metrics"],
    }

    audio_result = _train_audio_classification(datasets["audio_classification"])
    audio_path = output_dir / "audio_classification_model.joblib"
    _write_artifact(audio_result, audio_path)
    results["audio_classification"] = {
        "artifact": str(audio_path),
        "metrics": audio_result["metrics"],
        "labels": list(audio_result["label_encoder"].classes_),
    }

    anomaly_result = _train_anomaly_detection(datasets["anomaly_detection"])
    anomaly_path = output_dir / "anomaly_detection_model.joblib"
    _write_artifact(anomaly_result, anomaly_path)
    results["anomaly_detection"] = {
        "artifact": str(anomaly_path),
        "metrics": anomaly_result["metrics"],
    }

    metadata = {
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "artifacts": results,
    }
    _write_metadata(metadata, output_dir / "training_metadata.json")

    return results


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train dummy ML models.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Directory containing CSV datasets.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to store model artifacts.",
    )
    parser.add_argument(
        "--use-existing-only",
        action="store_true",
        help="Fail if datasets are missing instead of generating them.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    train_all(args.data_dir, args.output_dir, args.use_existing_only)


if __name__ == "__main__":
    main()
