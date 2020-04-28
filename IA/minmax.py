import math

from node import *

root_child = []

def minmax(state, max_depth, role):
    global root_child

    root_child = []
    root = Node(state)

    value = max_value(root, 0, max_depth, -math.inf, math.inf, role)

    for child in root_child:
        if child.getValue() == value:
            return child.getAction()

    return None

def max_value(node, current_depth, max_depth, alpha, beta, role):

    if current_depth == max_depth - 1:
        return heuristic(node, role) # TODO: fare euristica

    possible_moves = getPossibleMoves(node, role)

    node_value = -math.inf

    for move in possible_moves:

        next_state = nextState(node, move) # TODO: fare metodo nextState
        child_node = Node(next_state)

        node_value = math.max(node_value, min_value(child_node, current_depth + 1, max_depth, alpha, beta))
        child_node.setValue(node_value)

        if current_depth == 1:
            child_node.setAction(move)
            root_child.append(child_node)

        if node_value >= beta:
            return node_value

        alpha = math.max(alpha, node_value)

    return node_value

def min_value(node, current_depth, max_depth, alpha, beta, role):

    if current_depth == max_depth - 1:
        return heuristic(node) # TODO: fare euristica

    possible_moves = getPossibleMoves(node, role)

    node_value = math.inf

    for move in possible_moves:

        next_state = nextState(node, move)
        child_node = Node(next_state)

        node_value = math.min(node_value, max_value(child_node, current_depth + 1, max_depth, alpha, beta))
        child_node.setValue(node_value)

        if node_value <= alpha:
            return node_value

        beta = math.min(beta, node_value)

    return node_value
