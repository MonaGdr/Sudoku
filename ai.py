import random
from time import time
import json
from sim import *


# *** you can change everything except the name of the class, the act function and the sensor_data ***


class Agent:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        self.predicted_actions = []

    # the act function takes a json string as input
    # and outputs an action string
    # ('U' is go up,   'L' is go left,   'R' is go right,   'D' is go down,  'C' is clean tile)
    def act(self, percept):
        # ^^^ DO NOT change the act function above ***

        sensor_data = json.loads(percept)
        # ^^^ DO NOT change the sensor_data above ***

        # TODO implement your agent here

        if not self.predicted_actions:
            t_0 = time()
            initial_state = Simulator(sensor_data['map'], sensor_data['location'])
            self.predicted_actions = self.BFS_Search(initial_state)
            print('Run time: ', time() - t_0)

        action = self.predicted_actions.pop()
        return action

    def BFS_Search(self, root_game):
        interface = Interface()
        queue = [[root_game, []]]
        while queue:
            node = queue.pop(0)
            actions_list = interface.valid_actions(node)
            random.shuffle(actions_list)
            for action in actions_list:
                child_state = interface.copy_state(node[0])
                interface.evolve(child_state, action)
                queue.append([child_state, [action] + node[1]])
                if interface.goal_test(child_state): return [action] + node[1]
