import os
import sys

SCRIPT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.extend([SCRIPT_DIR, ROOT_DIR])

from pathlib import Path

import orchestrator
import visualize


def prompt_inputs():
    """Ask the user for required parameters and validate them."""
    image_path = input("Path to plant image file: ").strip()
    height_str = input("Plant height in cm: ").strip()
    age_str = input("Plant age in days: ").strip()

    errors = []
    if not Path(image_path).is_file():
        errors.append("Image file does not exist")

    try:
        height_cm = float(height_str)
        if height_cm <= 0:
            errors.append("Height must be a positive number")
    except ValueError:
        errors.append("Height must be numeric")

    try:
        days = int(age_str)
        if days <= 0:
            errors.append("Age must be a positive integer")
    except ValueError:
        errors.append("Age must be an integer")

    if errors:
        raise ValueError("; ".join(errors))

    return image_path, height_cm, days


def run_pipeline(image_path: str, height_cm: float, days: int):
    """Run the Cannabotica pipeline with the provided parameters."""
    Path('data').mkdir(exist_ok=True)

    graph = orchestrator.run_genspark(image_path)
    orchestrator.save_json(graph, 'data/plant_structure.json')

    timeline = orchestrator.run_manus(graph, height_cm=height_cm, days=days)
    orchestrator.save_json(timeline, 'data/growth_simulation.json')

    strategies = orchestrator.run_minimax(timeline)
    orchestrator.save_json(
        orchestrator.strategies_to_dicts(strategies),
        'data/strategic_plans.json'
    )

    print("Pipeline complete. Launching visualizer...")
    visualize.PlantVisualizer('data/plant_structure.json', 'data/growth_simulation.json')
    visualize.plt.show()


def main():
    try:
        params = prompt_inputs()
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    run_pipeline(*params)


if __name__ == '__main__':
    main()
