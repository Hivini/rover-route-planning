# route_finder
import math
import numpy as np

from typing import Tuple
from simpleai.search import SearchProblem


class RouteFinder(SearchProblem):

    def __init__(self, height_map: np.array, max_row: int, max_col: int, start: Tuple[int, int],
                 end: Tuple[int, int], max_height: float, invalid_height: int = None) -> None:
        self.height_map = height_map
        self.start = start
        self.end = end
        self.max_height = max_height
        self.invalid_height = invalid_height
        self.max_row = max_row
        self.max_col = max_col
        SearchProblem.__init__(self, self.start)

    def actions(self, state: Tuple[int, int]):
        """ Defines the valid actions that the agent can take depending on the state.

        The available movements for this are:
            - Up
            - Down
            - Left
            - Right
            - Diagonal right-up
            - Diagonal right-down
            - Diagonal left-up
            - Diagonal left-down
        """
        actions = []

        row = state[0]
        col = state[1]
        current_height = self.height_map[row][col]

        # Check what sides it can move
        move_left = col > 0
        move_right = col < self.max_col
        move_up = row > 0
        move_down = row < self.max_row

        if move_left:
            left = self.height_map[row][col - 1]
            if left != self.invalid_height and abs(current_height - left) < self.max_height:
                actions.append('ML')
        if move_right:
            right = self.height_map[row][col + 1]
            if right != self.invalid_height and abs(current_height - right) < self.max_height:
                actions.append('MR')
        if move_up:
            up = self.height_map[row - 1][col]
            if up != self.invalid_height and abs(current_height - up) < self.max_height:
                actions.append('MU')
        if move_down:
            down = self.height_map[row + 1][col]
            if down != self.invalid_height and abs(current_height - down) < self.max_height:
                actions.append('MD')
        if move_left and move_up:
            d_left_up = self.height_map[row - 1][col - 1]
            if d_left_up != self.invalid_height and abs(current_height - d_left_up) < self.max_height:
                actions.append('MDLU')
        if move_left and move_down:
            d_left_down = self.height_map[row + 1][col - 1]
            if d_left_down != self.invalid_height and abs(current_height - d_left_down) < self.max_height:
                actions.append('MDLD')
        if move_right and move_up:
            d_right_up = self.height_map[row - 1][col + 1]
            if d_right_up != self.invalid_height and abs(current_height - d_right_up) < self.max_height:
                actions.append('MDRU')
        if move_right and move_down:
            d_right_down = self.height_map[row + 1][col + 1]
            if d_right_down != self.invalid_height and abs(current_height - d_right_down) < self.max_height:
                actions.append('MDRD')
        return actions

    def result(self, state, action):
        """ The change of state.

        Updates the current coordinate depending on the movement.
        """
        # Move up
        if action == 'MU':
            return (state[0] - 1, state[1])
        elif action == 'MD':
            return (state[0] + 1, state[1])
        elif action == 'ML':
            return (state[0], state[1] - 1)
        elif action == 'MR':
            return (state[0], state[1] + 1)
        elif action == 'MDRU':
            return (state[0] - 1, state[1] + 1)
        elif action == 'MDRD':
            return (state[0] + 1, state[1] + 1)
        elif action == 'MDLD':
            return (state[0] + 1, state[1] - 1)
        elif action == 'MDLU':
            return (state[0] - 1, state[1] - 1)
    
    def is_goal(self, state):
        return state == self.end

    def cost(self, state, action, state2):
        """ The cost of the movement.

        In this case we set the cost to be 1 on sideways movements,
        and 1.5 for diagonal movements.
        """
        if action in ['MU', 'MD', 'ML', 'MR']:
            return 1
        return 1.5

    def heuristic(self, state):
        """ The heuristic used by the A* algorithm.

        We calculated the distance between the given state to the
        goal state by using Pythagoras theorem.
        """

        x = state[0]
        y = state[1]

        end_x = self.end[0]
        end_y = self.end[1]

        return math.sqrt(float(abs(end_x - x)**2 + abs(end_y - y)**2))

