import tkinter as tk
import numpy as np
import gymnasium as gym
from game import *

HEIGHT, WIDTH = 500, 500

class Env2048(tk.Tk):
    def __init__(self):
        super().__init__()
        print("This is the standard constructor of our environment class.")
        self.game = Game()  # Assuming you have a Game class for 2048 game logic
        self.canvas = self.build_canvas()
        self.canvas.pack()

        self.action_space = gym.spaces.Discrete(4)
        self._action_to_direction = {
            0: "up",
            1: "right",
            2: "down",
            3: "left"
        }

        self.observation_space = gym.spaces.Box(low=0, high=65536, shape=(4, 4), dtype=np.uint16)
        self.reward_range = [-np.inf, np.inf]

        self.reset()

    def build_canvas(self):
        canvas = tk.Canvas(self, bg='green', height=HEIGHT, width=WIDTH)

        # Create grid with 4x4 (4 rows with 4 columns)
        for c in range(0, WIDTH, WIDTH // 4):
            x1, y1, x2, y2 = c, 0, c, HEIGHT
            canvas.create_line(x1, y1, x2, y2)
        for r in range(0, HEIGHT, HEIGHT // 4):
            x1, y1, x2, y2 = 0, r, WIDTH, r
            canvas.create_line(x1, y1, x2, y2)

        return canvas

    def render(self):
        print(self.game.matrix)

    def reset(self):
        print("This resets the environment.")
        self.game.reset()

    def step(self, action):
        print("This takes an action and updates the environment.")
        assert self.action_space.contains(action)
        self.game.take_action(self._action_to_direction[action])
        return self.game.matrix, self.game.score, self.game.game_over(), {}

if __name__ == "__main__":
    env = Env2048()
    env.mainloop()
