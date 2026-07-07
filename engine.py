from predictor import Predictor
from explainability import ExplainabilityEngine


class PredictionEngine:
    def __init__(self, segment_model):
        self.predictor = Predictor(segment_model)
        self.explainer = ExplainabilityEngine(segment_model)

    def predict(self, features: dict):
        prediction = self.predictor.predict(features)

        prediction["explanation"] = {
            "drivers": self.explainer.explain(features)
        }

        prediction["metadata"] = {
            "model": "XGBoost",
            "calibrated": True,
            "version": "1.0.0",
        }

        return prediction