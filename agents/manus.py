import copy

class Node:
    def __init__(self, id, type, pos, age_days, parent=None, topped=False, stressed=False):
        self.id = id
        self.type = type  # τώρα ταιριάζει με το JSON
        self.pos = pos
        self.age_days = age_days
        self.parent = parent
        self.topped = topped
        self.stressed = stressed
        self.children = []

    def grow(self, growth_factor=1.0):
        if not self.topped:
            # Βεβαιώσου ότι pos έχει 3 στοιχεία
            while len(self.pos) < 3:
                self.pos.append(0)
            self.pos[2] += growth_factor
        self.age_days += 1

class PlantSimulator:
    def __init__(self, graph_json):
        self.nodes = {node['id']: Node(
            id=node['id'],
            type=node['type'],  # εδώ παίρνει το 'type' σωστά
            pos=node['pos'],
            age_days=node['age_days'],
            parent=node.get('parent')
        ) for node in graph_json['nodes']}
        self.edges = graph_json['edges']
        for edge in self.edges:
            parent = self.nodes[edge['from']]
            child = self.nodes[edge['to']]
            parent.children.append(child.id)
        self.day = 0

    def simulate_day(self):
        self.day += 1
        for node in self.nodes.values():
            node.grow(growth_factor=1.0)
        # Εδώ μπορούμε να βάλουμε logic για topping, supercropping, fimming

    def get_state_json(self):
        return {
            "day": self.day,
            "nodes": [
                {
                    "id": n.id,
                    "type": n.type,
                    "pos": n.pos,
                    "age_days": n.age_days,
                    "parent": n.parent,
                    "topped": n.topped,
                    "stressed": n.stressed
                }
                for n in self.nodes.values()
            ]
        }

def run_simulation(graph_json, days=35):
    sim = PlantSimulator(graph_json)
    timeline = []
    for _ in range(days):
        sim.simulate_day()
        if sim.day in [7, 14, 21, 35]:
            timeline.append(sim.get_state_json())
    return timeline

if __name__ == "__main__":
    # Εδώ τοποθέτησε ένα mock graph για το test
    mock_graph = {
        "nodes": [
            {"id": "n1", "type": "apical", "pos": [0, 0, 0], "age_days": 14, "parent": None},
            {"id": "n2", "type": "side", "pos": [1, 0, 0], "age_days": 7, "parent": "n1"}
        ],
        "edges": [{"from": "n1", "to": "n2"}]
    }
    timeline = run_simulation(mock_graph)
    for state in timeline:
        print(state)
