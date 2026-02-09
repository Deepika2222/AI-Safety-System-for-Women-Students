"""
Dataset utilities for training dummy ML models.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Tuple

import numpy as np
import pandas as pd


DATA_DIR = Path(__file__).resolve().parent / "data"


@dataclass
class DatasetSpec:
    filename: str
    generator: Callable[[int], pd.DataFrame]
    min_rows: int


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


def generate_risk_scoring_dataset(num_rows: int = 300) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    features = rng.normal(0, 1, size=(num_rows, 5))
    weights = np.array([0.9, -0.4, 0.6, -0.3, 0.2])
    logits = features @ weights + rng.normal(0, 0.3, size=num_rows)
    probs = _sigmoid(logits)
    labels = (probs > 0.5).astype(int)

    columns = [f"feature_{i}" for i in range(1, 6)]
    df = pd.DataFrame(features, columns=columns)
    df["label"] = labels
    return df


def generate_audio_classification_dataset(num_rows: int = 320) -> pd.DataFrame:
    rng = np.random.default_rng(7)
    classes = ["normal", "scream", "distress", "alarm"]
    features = []
    labels = []

    for idx, label in enumerate(classes):
        class_rows = num_rows // len(classes)
        mean = (idx + 1) * 0.8
        class_features = rng.normal(mean, 0.6, size=(class_rows, 10))
        features.append(class_features)
        labels.extend([label] * class_rows)

    features = np.vstack(features)
    columns = [f"feature_{i}" for i in range(1, 11)]
    df = pd.DataFrame(features, columns=columns)
    df["label"] = labels
    return df


def generate_anomaly_detection_dataset(num_rows: int = 360) -> pd.DataFrame:
    rng = np.random.default_rng(21)
    normal_rows = int(num_rows * 0.85)
    anomaly_rows = num_rows - normal_rows

    normal = rng.normal(0, 1, size=(normal_rows, 6))
    anomalies = rng.normal(4, 1.5, size=(anomaly_rows, 6))

    features = np.vstack([normal, anomalies])
    labels = np.array([0] * normal_rows + [1] * anomaly_rows)

    columns = [f"feature_{i}" for i in range(1, 7)]
    df = pd.DataFrame(features, columns=columns)
    df["label"] = labels
    return df


def _ensure_dataset(path: Path, generator: Callable[[int], pd.DataFrame], min_rows: int) -> pd.DataFrame:
    if path.exists():
        df = pd.read_csv(path)
        if len(df) >= min_rows:
            return df
    df = generator(max(min_rows, 50))
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def load_datasets(data_dir: Path | None = None, use_existing_only: bool = False) -> Dict[str, pd.DataFrame]:
    base_dir = data_dir or DATA_DIR
    base_dir.mkdir(parents=True, exist_ok=True)

    specs: Dict[str, DatasetSpec] = {
        "risk_scoring": DatasetSpec(
            filename="risk_scoring.csv",
            generator=generate_risk_scoring_dataset,
            min_rows=120,
        ),
        "audio_classification": DatasetSpec(
            filename="audio_classification.csv",
            generator=generate_audio_classification_dataset,
            min_rows=160,
        ),
        "anomaly_detection": DatasetSpec(
            filename="anomaly_detection.csv",
            generator=generate_anomaly_detection_dataset,
            min_rows=180,
        ),
    }

    datasets: Dict[str, pd.DataFrame] = {}
    for name, spec in specs.items():
        path = base_dir / spec.filename
        if use_existing_only:
            if not path.exists():
                raise FileNotFoundError(f"Missing dataset: {path}")
            datasets[name] = pd.read_csv(path)
            continue
        datasets[name] = _ensure_dataset(path, spec.generator, spec.min_rows)

    return datasets


def split_features_labels(df: pd.DataFrame, label_column: str = "label") -> Tuple[pd.DataFrame, pd.Series | None]:
    if label_column not in df.columns:
        return df.copy(), None
    features = df.drop(columns=[label_column])
    labels = df[label_column]
    return features, labels
