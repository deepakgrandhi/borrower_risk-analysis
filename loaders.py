from pathlib import Path

import joblib

from scoring import ScoreCalculator
import shap

MODELS_DIR = Path("models")


class SegmentModel:
    def __init__(self, name: str, bundle_path: Path, constants_path: Path):
        bundle = joblib.load(bundle_path)
        constants = joblib.load(constants_path)

        self.name = name
        self.model = bundle["model"]
        self.calibrator = bundle["calibrator"]
        self.features = bundle["features"]
        self.reason_map = bundle["reason_map"]
        self.explainer = shap.TreeExplainer(self.model)

        self.scorer = ScoreCalculator(
            factor=constants["FACTOR"],
            offset=constants["OFFSET"],
        )


def load_retail_model():
    return SegmentModel(
        "Retail",
        MODELS_DIR / "retail_bundle.pkl",
        MODELS_DIR / "constants.pkl",
    )


def load_sme_model():
    return SegmentModel(
        "SME",
        MODELS_DIR / "sme_bundle.pkl",
        MODELS_DIR / "constants.pkl",
    )