import json
from pathlib import Path

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def run_genspark(image_path=None):
    """Run the Genspark agent.

    Parameters
    ----------
    image_path : str, optional
        Path to an image file of the plant. The current mock implementation
        simply validates the path and generates an example graph.
    """
    from agents.genspark import PlantGraph

    if image_path and not Path(image_path).is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    plant = PlantGraph()
    if image_path:
        plant.build_from_image(image_path)
    else:
        plant.build_example()
    return plant.to_json()

def run_manus(graph_json, height_cm=100.0, days=35):
    """Run the Manus growth simulation.

    Parameters
    ----------
    graph_json : dict
        Plant structure as produced by Genspark.
    height_cm : float
        Target plant height for the simulated period.
    days : int
        Number of days to simulate.
    """
    from agents.manus import run_simulation

    timeline = run_simulation(graph_json, days=days, target_height_cm=height_cm)
    return timeline

def run_minimax(timeline):
    # Προσομοίωση κλήσης minimax module
    from agents.minimax import generate_strategies
    strategies = generate_strategies()
    return strategies

def strategies_to_dicts(strategies):
    return [
        {
            "name": s.name,
            "actions": s.actions,
            "projections": s.projections,
            "evaluation": s.evaluation
        }
        for s in strategies
    ]

def main(image_path=None, height_cm=100.0, days=35):
    """Run the full Cannabotica pipeline."""
    print("Running Genspark...")
    graph = run_genspark(image_path)
    save_json(graph, 'data/plant_structure.json')

    print("Running Manus...")
    timeline = run_manus(graph, height_cm=height_cm, days=days)
    save_json(timeline, 'data/growth_simulation.json')

    print("Running Minimax...")
    strategies = run_minimax(timeline)
    strategies_dicts = strategies_to_dicts(strategies)
    save_json(strategies_dicts, 'data/strategic_plans.json')

    print("Orchestration complete. Outputs saved to data/")

if __name__ == "__main__":
    Path('data').mkdir(exist_ok=True)
    main()
