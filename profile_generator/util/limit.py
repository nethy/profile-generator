def limit(a: float, lower_bound: float = 0.0, uppper_bound: float = 1.0) -> float:
    return max(lower_bound, min(uppper_bound, a))
