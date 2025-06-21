class Node:
    def __init__(self, id, node_type, pos, age_days, parent=None):
        self.id = id
        self.type = node_type
        self.pos = pos
        self.age_days = age_days
        self.parent = parent
        self.children = []

class PlantGraph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.id] = node
        if node.parent:
            self.nodes[node.parent].children.append(node.id)

    def build_example(self):
        n1 = Node("n1", "apical", [0,0,0], 14)
        n2 = Node("n2", "side", [1,0,0], 7, parent="n1")
        self.add_node(n1)
        self.add_node(n2)

    def build_from_image(self, image_path):
        """Placeholder image processing.

        Parameters
        ----------
        image_path : str
            Path to the plant image. The current implementation does not parse
            the image but ensures that the file exists and then builds the
            example graph.
        """
        with open(image_path, 'rb'):
            pass  # just validate that the image can be read
        self.build_example()

    def to_json(self):
        return {
            "nodes": [
                {"id": n.id, "type": n.type, "pos": n.pos, "age_days": n.age_days, "parent": n.parent}
                for n in self.nodes.values()
            ],
            "edges": [
                {"from": n.parent, "to": n.id} for n in self.nodes.values() if n.parent
            ]
        }

if __name__ == "__main__":
    plant = PlantGraph()
    plant.build_example()
    print(plant.to_json())
