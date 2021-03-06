"""Main program for keyboard agent
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import Agent as AG
import SuperMarioBros as SMB

config = SMB.simulation_config

layout = SMB.layout_fromdefault()

host = SMB.instantiate_malmo(layout)

render = SMB.Renderer(host)

simulation = SMB.MarioSimulation(layout, config=config)

# keypoller = SMB.KeyPoller()

AG.keyboard_agent(simulation, render, config=config)
