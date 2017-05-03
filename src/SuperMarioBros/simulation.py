"""Running world simulations of Super Mario Bros
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import numpy as np

from __init__ import *


def layout_tobb(layout, config=None):
    maxx, maxy = layout.shape

    id2block = {0: 'air', 1: 'brick_block', 2: 'lava',
                3: 'red_mushroom'} if config is None or "id2block" not in config else config["id2block"]
    block2id = dict(map(lambda item: (item[1], item[0]), id2block.items()))
    block_radius = (0.5, 0.5) if config is None or "block_radius" not in config else config["block_radius"]
    pos2bb = {}

    for x in range(maxx):
        for y in range(maxy):
            if layout[x, y] != block2id['air']:
                pos2bb[(x, y)] = CollidableAABB((x, y), block_radius, config)

    return pos2bb


def collision_proposal(mario, pos2bb, config=None):
    """
    Propose potential collision box around mario
    :param mario: CollidableRigid instance
    :param pos2bb: Position-to-boundingbox mapping
    :param config: Global configuration
    :return: List of potential collision boxes
    """
    minx, miny, maxx, maxy = -2, -2, 3, 3

    return list(map(lambda pos: pos2bb[pos],
                    filter(lambda pos: pos in pos2bb,
                           map(lambda d: tuple(np.trunc(mario.get_center() + d).astype("int")),
                               it.product(xrange(minx, maxx), xrange(miny, maxy))))))


def hit_edge_reaction(collision):
    """
    Give corresponding handler to each edge hit.
    Normal line indexed directions: 0: right, 1: left, 2: up, 3: down
    :param collision: Collision dict
    :return: Hit handler
    """
    directions = np.array([[1.0, -1.0, 0.0, 0.0], [0.0, 0.0, 1.0, -1.0]])
    edge2action = {0: hit_sides, 1: hit_sides, 2: hit_ground, 3: hit_ceiling}

    return edge2action[np.argmax(np.dot(collision['hit']['normal'], directions))]


class MarioSimulation:
    def __init__(self, layout, config=None):
        """
        Instantiate physics engine objects
        :param layout: Two-dimensional numpy array layout
        :param config: Global configuration
        """
        self.layout = layout
        self.config = config

        init_pos = np.array([0, 2, 0]) if config is None or "init_pos" not in config else config["init_pos"]
        mario_bb = np.array([0.5, 1]) if config is None or "mario_bb" not in config else config["mario_bb"]

        self.mario = CollidableRigid(init_pos, mario_bb, config)
        self.brick_bb = layout_tobb(layout, config)

    def run(self, input, observer, action):
        """
        Main loop of game simulation
        :param input: Input module, callable or with poll() function
        :param observer: Observation receiver
        :param action: Action module, callable or with act() function
        :return: None
        """
        # Advance a time step
        self.mario.update()

        # Locate blocks for collision detections
        bb_to_check = collision_proposal(self.mario, self.brick_bb, self.config)

        # Resolve collisions
        collisions = list(filter(lambda pair: pair[1]['hit'] is not None,
                                 map(lambda bb: (bb.get_center(), bb.collide(self.mario)), bb_to_check)))

        closest_collision = min(collisions, key=lambda pair: pair[1]['hit']['time'])

        self.mario.reaction(collision_resolved, closest_collision[1]["hit"]["delta"])

        # Process momentum change
        self.mario.reaction(hit_edge_reaction(closest_collision[1]))

        # Take an observation

        # Take an action
        return closest_collision