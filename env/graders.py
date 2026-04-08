def clamp_score(raw_score: float) -> float:
    """Ensure score falls within strictly bounded [0.01, 0.99]"""
    return max(0.01, min(raw_score, 0.99))
