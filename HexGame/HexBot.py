'''
Applying MCTS
'''

from consts import *
from funcs import *
from math import sqrt, log
from time import clock
import random


class Node:
    def __init__(self, state=None, move=None, parent=None):
        self.state = state
        self.move = move
        self.parent = parent
        self.children = {}
        self.num_wins = 0;
        self.num_simuls = 0;
        self.value = NEG_INFINITY

    def update_value(self):
        if (self.value == NEG_INFINITY):
            exploitation = float(self.num_wins / self.num_simuls);
            exploration = float(sqrt(2 * log(self.parent.num_simuls) / self.num_simuls))
            self.value = exploitation + exploration

class HexBot:
    def __init__(self, play_color):
        self.play_color = play_color
        self.time_per_move = TIME_PER_MOVE

    def set_root(self, state):
        self.root = Node(state)

    '''
        Find the child node that has maximum value
    '''
    def find_max_node(self, node):
        max_node = Node()
        max_nodes = []

        for child in node.children:
            if (max_node.value < child.value):
                max_node = child

        for child in node.children:
            if (child.value == max_node.value):
                max_nodes.append(child)

        return random.choice(max_nodes)

    def MCTS(self):

        start = clock()
        time_limit = start + self.time_per_move - 3

        '''Searching to find the winning move'''
        current_node = self.root
        while clock() < time_limit:

            if len(current_node.children): #selection
                current_node = self.find_max_node(current_node)
            elif game_status(current_node.state) == UNKNOWN: #expansion
                available_moves = find_empty_cells(current_node.state)

                for move in available_moves: # add children
                    # define child
                    new_state = current_node.state
                    new_state[move[0]][move[1]] = self.play_color
                    child = Node(new_state, move, current_node)

                    # add child by its move
                    current_node.children[child.move] = child

                current_node = random.choice(list(current_node.children.values()))

            current_state = current_node.state
            outcome = self.simulation(current_state)
            self.back_propagation(current_node, outcome)

    def simulation(self, state):
        available_moves = find_empty_cells(state)

        while (game_status(state) == UNKNOWN):
            move = random(available_moves)
            available_moves.remove(move)

            state[move[0]][move[1]] = self.play_color

        return game_status(state)

    def back_propagation(self, node, outcome):
        point = 0
        if outcome == self.play_color:
            point = 1
        elif outcome == DRAW:
            point = 0.5

        while node != None:
            node.num_wins += point
            node.num_simuls += 1

            node = node.parent
