import math


class ScoreCalculator:
    def __init__(self, factor: float, offset: float):
        self.factor = factor
        self.offset = offset

    def probability_to_score(self, probability: float) -> float:
        probability = min(max(probability, 1e-6), 1 - 1e-6)
        odds = (1 - probability) / probability
        return self.offset + self.factor * math.log(odds)

    @staticmethod
    def score_to_tier(score: float) -> str:
        if score >= 750:
            return "Low"
        if score >= 650:
            return "Medium"
        if score >= 550:
            return "High"
        return "Critical"