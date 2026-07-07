import pandas as pd


class Predictor:
    def __init__(self, segment_model):
        self.segment_model = segment_model

    def predict(self, features: dict):
        missing = [
            feature
            for feature in self.segment_model.features
            if feature not in features
        ]

        if missing:
            raise ValueError(
                f"Missing required features: {missing}"
            )

        row = pd.DataFrame([features])
        row = row[self.segment_model.features]

        raw_probability = self.segment_model.model.predict_proba(row)[:, 1]

        probability = float(
            self.segment_model.calibrator.predict(raw_probability)[0]
        )

        score = float(
            self.segment_model.scorer.probability_to_score(probability)
        )

        tier = self.segment_model.scorer.score_to_tier(score)

        return {
            "segment": self.segment_model.name,
            "prediction": {
                "probability": probability,
                "score": score,
                "tier": tier,
            },
        }