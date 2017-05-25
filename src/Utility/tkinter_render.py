"""Tkinter-based render for visualization
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import Tkinter as tk


class TKRender:
    def __init__(self, layout, config=None):
        # Difference in tkinter coordinate system and ours:
        # Flip the y-axis
        maxx, maxy = layout.shape
        self.shape = layout.shape
        id2block = config["id2block"]
        init_pos = config["init_pos"]

        self.root = tk.Tk()
        self.root.resizable(0, 0)
        self.canvas = tk.Canvas(master=self.root, width=maxx * 16, height=maxy * 16)
        self.canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.pos2bb = dict((id2block[k], {}) for k in id2block if id2block[k] != 'air')
        for x in range(maxx):
            for y in range(maxy):
                if id2block[layout[x, y]] != 'air':
                    self.pos2bb[id2block[layout[x, y]]][x, y] = self.canvas.create_rectangle(
                        x * 16, (maxy - y - 1) * 16, (x + 1) * 16, (maxy - y) * 16,
                        fill=config["block2color"][id2block[layout[x, y]]])

        self.mario = self.canvas.create_rectangle(
            init_pos[0] * 16, (maxy - init_pos[1] - 1.5) * 16, (init_pos[0] + 1) * 16, (maxy - init_pos[1] + 0.5) * 16,
            fill=config["block2color"]["mario"])

    def render(self, rigid):
        displacement = rigid.displacement_difference()
        self.canvas.move(self.mario, displacement[0] * 16, -displacement[1] * 16)
        self.root.update_idletasks()
        self.root.update()
