import math

from common.utils import calculate_hash


class Node:
    def __init__(self, value: str, left_child=None, right_child=None):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child


def compute_tree_depth(number_of_leaves: int) -> int:
    return math.ceil(math.log2(number_of_leaves))


def is_power_of_2(number_of_leaves: int) -> bool:
    return math.log2(number_of_leaves).is_integer()


def fill_set(list_of_nodes: list):
    current_number_of_leaves = len(list_of_nodes)
    if is_power_of_2(current_number_of_leaves):
        return list_of_nodes
    total_number_of_leaves = 2**compute_tree_depth(current_number_of_leaves)
    if current_number_of_leaves % 2 == 0:
        for i in range(current_number_of_leaves, total_number_of_leaves, 2):
            list_of_nodes = list_of_nodes + [list_of_nodes[-2], list_of_nodes[-1]]
    else:
        for i in range(current_number_of_leaves, total_number_of_leaves):
            list_of_nodes.append(list_of_nodes[-1])
    return list_of_nodes


def build_merkle_tree(node_data: [str]) -> Node:
    complete_set = fill_set(node_data)
    old_set_of_nodes = [Node(calculate_hash(data)) for data in complete_set]
    tree_depth = compute_tree_depth(len(old_set_of_nodes))

    for i in range(0, tree_depth):
        num_nodes = 2**(tree_depth-i)
        new_set_of_nodes = []
        for j in range(0, num_nodes, 2):
            child_node_0 = old_set_of_nodes[j]
            child_node_1 = old_set_of_nodes[j+1]
            new_node = Node(
                value=calculate_hash(f"{child_node_0.value}{child_node_1.value}"),
                left_child=child_node_0,
                right_child=child_node_1
            )
            new_set_of_nodes.append(new_node)
        old_set_of_nodes = new_set_of_nodes
    return new_set_of_nodes[0]
