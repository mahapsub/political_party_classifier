class Node:
    def __init__(self, label=None, children=None, mode=None): #children = ("branch", node)
        self.label = label
        self.children = children  # children of 'branch' --> node
        self.mode = mode
    # you may want to add additional fields here...
    def create_node(label, attribute_values):
        new_node = Node(label)
        children = {}
        for val in attribute_values:
            children[val] = None
        new_node.children = children
        return new_node
