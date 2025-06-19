import json
from pathlib import Path

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def run_genspark():
    # Προσομοίωση κλήσης genspark module
    from agents.genspark import PlantGraph
    plant = PlantGraph()
    plant.build_example()
    return plant.to_json()

def run_manus(graph_json):
    # Προσομοίωση κλήσης manus module
    from agents.manus import run_simulation
    timeline = run_simulation(graph_json)
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

def main():
    print("Running Genspark...")
    graph = run_genspark()
    save_json(graph, 'data/plant_structure.json')

    print("Running Manus...")
    timeline = run_manus(graph)
    save_json(timeline, 'data/growth_simulation.json')

    print("Running Minimax...")
    strategies = run_minimax(timeline)
    strategies_dicts = strategies_to_dicts(strategies)
    save_json(strategies_dicts, 'data/strategic_plans.json')

    print("Orchestration complete. Outputs saved to data/")

if __name__ == "__main__":
    Path('data').mkdir(exist_ok=True)
    main()
