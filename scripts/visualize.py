import json
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import for 3D


def load_json(path):
    """Load JSON data from a file."""
    with open(path, 'r') as f:
        return json.load(f)


class PlantVisualizer:
    """Interactive matplotlib visualizer for plant growth."""

    def __init__(self, plant_path: str, timeline_path: str):
        self.plant_path = plant_path
        self.timeline_path = timeline_path
        self.timeline = load_json(self.timeline_path)
        if not self.timeline:
            raise ValueError("Growth timeline is empty")
        self.index = 0

        self.fig = plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.set_box_aspect((1, 1, 1))  # keep aspect ratio
        try:
            self.fig.canvas.manager.set_window_title("Cannabotica Visualizer")
        except Exception:
            pass

        self.fig.canvas.mpl_connect("key_press_event", self.on_key)
        self.draw_state()

    def draw_state(self):
        """Draw the current state of the plant."""
        self.ax.clear()
        state = self.timeline[self.index]

        nodes = {n["id"]: n for n in state["nodes"]}

        # Draw branches
        for node in state["nodes"]:
            parent_id = node.get("parent")
            if parent_id and parent_id in nodes:
                parent = nodes[parent_id]
                xs = [parent["pos"][0], node["pos"][0]]
                ys = [parent["pos"][1], node["pos"][1]]
                zs = [parent["pos"][2], node["pos"][2]]
                self.ax.plot(xs, ys, zs, color="gray", linewidth=1)

        # Draw nodes and shoots
        for node in state["nodes"]:
            x, y, z = node["pos"]
            is_apical = node["type"] == "apical"
            color = "forestgreen" if is_apical else "royalblue"
            if node.get("topped"):
                color = "crimson"
            elif node.get("stressed"):
                color = "darkorange"

            size = 120 if is_apical else 60
            self.ax.scatter(x, y, z, s=size, color=color, edgecolor="k", zorder=5)

            # Shoots as small cross like branches
            shoot_len = 0.3
            directions = [
                (shoot_len, 0, shoot_len),
                (-shoot_len, 0, shoot_len),
                (0, shoot_len, shoot_len),
                (0, -shoot_len, shoot_len),
            ]
            for dx, dy, dz in directions:
                self.ax.plot(
                    [x, x + dx],
                    [y, y + dy],
                    [z, z + dz],
                    color=color,
                    linewidth=1,
                )

        self.ax.set_title(f"Day {state['day']}")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        plt.tight_layout()
        plt.draw()

    def on_key(self, event):
        """Handle left/right key events for navigation."""
        if event.key in ['right', 'd']:
            if self.index < len(self.timeline) - 1:
                self.index += 1
                self.draw_state()
        elif event.key in ['left', 'a']:
            if self.index > 0:
                self.index -= 1
                self.draw_state()


def main():
    plant_path = os.path.join('data', 'plant_structure.json')
    timeline_path = os.path.join('data', 'growth_simulation.json')

    if not os.path.exists(plant_path) or not os.path.exists(timeline_path):
        print('Plant data not found. Run the orchestrator first.')
        return

    PlantVisualizer(plant_path, timeline_path)
    plt.show()


if __name__ == '__main__':
    main()
