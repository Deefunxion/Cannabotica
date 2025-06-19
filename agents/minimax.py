class Strategy:
    def __init__(self, name, actions, projections, evaluation):
        self.name = name
        self.actions = actions  # list of dicts: {"node_id": ..., "action": ...}
        self.projections = projections  # list of dicts: day, height_cm, canopy_spread_cm
        self.evaluation = evaluation  # dict with metrics like yield_estimate, canopy_evenness_score

def generate_strategies():
    # Παράδειγμα 3 στρατηγικών
    strategies = []

    strategies.append(
        Strategy(
            "Max Yield",
            [{"node_id": "n8", "action": "top"}, {"node_id": "n5", "action": "supercrop"}],
            [{"day": 7, "height_cm": 90, "canopy_spread_cm": 40}, {"day": 14, "height_cm": 110, "canopy_spread_cm": 50}],
            {"yield_estimate": 1200, "canopy_evenness_score": 85, "stealth_height_score": 40}
        )
    )
    # Πρόσθεσε άλλες στρατηγικές εδώ αν θες

    return strategies

if __name__ == "__main__":
    strategies = generate_strategies()
    for strat in strategies:
        print(f"Strategy: {strat.name}")
        print(f"Actions: {strat.actions}")
        print(f"Projections: {strat.projections}")
        print(f"Evaluation: {strat.evaluation}")
        print()
