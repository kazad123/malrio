"""Main program for testing search agent
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"


import time
import numpy as np
import SuperMarioBros as SMB
import Supervised as SV
import Agent as AG


config = SMB.simulation_config

layout = SMB.layout_asblank()

host = SMB.instantiate_malmo(layout)

render = SMB.Renderer(host)

simulation = SMB.MarioSimulation(layout, config=config)

AG.test_agent(simulation, render, config=config)