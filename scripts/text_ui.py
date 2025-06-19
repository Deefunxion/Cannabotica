import json

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def print_plant_structure(data):
    print("\nPlant Structure:")
    for node in data['nodes']:
        print(f"Node {node['id']}: Type={node['type']}, Pos={node['pos']}, Age={node['age_days']}, Parent={node['parent']}")

def print_growth_simulation(data):
    print("\nGrowth Simulation Timeline:")
    for state in data:
        print(f"Day {state['day']}:")
        for node in state['nodes']:
            print(f"  Node {node['id']} pos={node['pos']}, age={node['age_days']}")

def print_strategic_plans(data):
    print("\nStrategic Plans:")
    for strat in data:
        print(f"Strategy: {strat['name']}")
        print(f"  Actions: {strat['actions']}")
        print(f"  Evaluation: {strat['evaluation']}")

def main():
    plant = load_json('data/plant_structure.json')
    growth = load_json('data/growth_simulation.json')
    strategies = load_json('data/strategic_plans.json')

    print_plant_structure(plant)
    print_growth_simulation(growth)
    print_strategic_plans(strategies)

if __name__ == "__main__":
    main()
