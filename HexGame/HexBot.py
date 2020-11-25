'''
Applying MCTS
'''

from consts import *
from funcs import *
from math import sqrt, log
from time import clock
import copy
import random


class Node:
    def __init__(self, state=None, move=None, parent=None):
        self.state = state
        self.move = move
        self.parent = parent
        self.children = []
        self.num_wins = 0.0
        self.num_simuls = 0.0
        self.value = NEG_INFINITY

    def update_value(self):
        if self.value == NEG_INFINITY:
            exploitation = float(self.num_wins / self.num_simuls)
            exploration = float(sqrt(2 * log(self.parent.num_simuls) / self.num_simuls))
            self.value = float(exploitation + exploration)

class HexBot:
    def __init__(self, play_color, state):
        self.play_color = play_color
        self.time_per_move = TIME_PER_MOVE
        self.root = Node(state)

    def set_root(self, state):
        self.root = Node(state)

    '''
        Find the child node that has maximum value
    '''
    def find_max_node(self, node):
        max_node = Node()
        max_nodes = []

        if len(node.children) > 0:
            for child in node.children:
                if child.num_simuls > 0:
                    child.update_value()
                if max_node.value < child.value:
                    max_node = child

            for child in node.children:
                if child.value == max_node.value:
                    max_nodes.append(child)

            max_node = random.choice(max_nodes)

        return max_node

    def MCTS(self):

        start = clock()
        time_limit = start + self.time_per_move

        '''Searching to find the winning move'''
        current_node = self.root
        player = self.play_color

        while clock() < time_limit:

            current_node, current_state, player = self.selection_expansion(player) # selection + expansion

            outcome = self.simulation(current_state, player)[1]

            print("Outcome: " + str(outcome))
            print("Player: " + str(player))
            self.back_propagation(current_node, outcome, player)

    def selection_expansion(self, player):
        current_node = self.root
        current_state = copy.deepcopy(self.root.state)

        while len(current_node.children) > 0:
            current_node = self.find_max_node(current_node)

            if current_node.value == NEG_INFINITY:
                return current_node, current_state, 3 - player

        if game_status(current_node.state) == UNKNOWN:  # expansion
            #available_moves = find_empty_cells(current_node.state)
            available_moves = find_empty_neighbor(current_node.state)

            for move in available_moves:  # add children
                # define child
                new_state = copy.deepcopy(current_node.state)
                new_state[move[0]][move[1]] = player
                child = Node(new_state, move, current_node)

                # add child
                current_node.children.append(child)
            print("number of children: " + str(len(current_node.children)))

            current_node = random.choice(current_node.children)
            current_state = copy.deepcopy(current_node.state)

            return current_node, current_state, 3 - player

        return current_node, current_state, player

    def simulation(self, state, player):
        available_moves = find_empty_cells(state)


        # random
        while game_status(state) == UNKNOWN:
            move = random.choice(available_moves)
            available_moves.remove(move)

            state[move[0]][move[1]] = player
            player = 3 - player

        return None, game_status(state)

        #print("Game status: " + str(game_status(state)))


        '''
            apply negamax
        '''

        status = game_status(state)
        max_score = NEG_INFINITY

        if status != UNKNOWN:
            if status == 3 - self.play_color:
                max_score = -1
            elif status == DRAW:
                max_score = 0
            elif status == self.play_color:
                max_score = 1

            return max_score, status

        new_player = player
        for move in available_moves:
            new_state = state
            new_state[move[0]][move[1]] = new_player
            new_player = 3 - new_player

            score = self.simulation(new_state, new_player)[0]

            if max_score < score:
                max_score = score

            if max_score >= 1:
                break

        #print("Max_score: " + str(max_score))
        if max_score > 0:
            return max_score, self.play_color
        elif max_score == 0:
            return max_score, DRAW
        else:
            return max_score, 3 - self.play_color

    def back_propagation(self, node, outcome, player):
        point = -1.0

        if outcome == 3 - player:
            point = 1.0
        elif outcome == DRAW:
            point = 0.5

        while node is not None:
            node.num_wins += point
            node.num_simuls += 1.0

            node = node.parent

            if point == 1.0:
                point = -1.0
            elif point == -1.0:
                point = 1.0

    def make_best_move(self):

        self.MCTS()
        best_node = self.find_max_node(self.root)

        print("Best Value: " + str(best_node.value))
        return best_node.move
