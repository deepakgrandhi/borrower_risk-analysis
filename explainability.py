import pandas as pd


class ExplainabilityEngine:
    def __init__(self, segment_model):
        self.segment_model = segment_model

    def explain(self, feature_dict: dict, top_n: int = 3):
        row = pd.DataFrame([feature_dict])

        row = row[self.segment_model.features]

        shap_values = self.segment_model.explainer.shap_values(row)[0]

        points = (
            -shap_values
            * self.segment_model.scorer.factor
        )

        grouped = {}

        for feature, point in zip(
            self.segment_model.features,
            points,
        ):
            reason = self.segment_model.reason_map.get(
                feature,
                "Other",
            )

            grouped[reason] = (
                grouped.get(reason, 0.0)
                + float(point)
            )

        ranked = sorted(
            grouped.items(),
            key=lambda item: abs(item[1]),
            reverse=True,
        )

        drivers = [
            {
                "reason": reason,
                "impact": impact,
            }
            for reason, impact in ranked[:top_n]
        ]

        return drivers