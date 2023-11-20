import tkinter as tk
import pandas as pd
import numpy as np
import time

class QLearningTable:
    # Initialize parameters and create a Q-table
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def choose_action(self, observation):
        self.check_state_exist(observation)
        if np.random.uniform() < self.epsilon:
            state_action = self.q_table.loc[observation, :]
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()
        else:
            q_target = r
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            new_row = pd.Series([0] * len(self.actions), index=self.q_table.columns, name=state)
            self.q_table = pd.concat([self.q_table, new_row])

class Maze(tk.Tk):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(4 * 40, 4 * 40))
        self.build_maze()

    def build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                                height=4 * 40,
                                width=4 * 40)

        for c in range(0, 4 * 40, 40):
            x0, y0, x1, y1 = c, 0, c, 4 * 40
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, 4 * 40, 40):
            x0, y0, x1, y1 = 0, r, 4 * 40, r
            self.canvas.create_line(x0, y0, x1, y1)

        # origin
        origin = np.array([60, 60])  # middle of maze (1, 1)
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        # hell
        hell_center = np.array([100, 100])  # center of maze (2, 2)
        self.hell = self.canvas.create_rectangle(
            hell_center[0] - 15, hell_center[1] - 15,
            hell_center[0] + 15, hell_center[1] + 15,
            fill='black')

        # goal
        oval_center = np.array([140, 140])  # bottom of maze (3, 3)
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')

        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        origin = np.array([60, 60])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        return self.canvas.coords(self.rect)

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 'u':
            if s[1] > 40:
                base_action[1] -= 40
        elif action == 'd':
            if s[1] < (4 - 1) * 40:
                base_action[1] += 40
        elif action == 'r':
            if s[0] < (4 - 1) * 40:
                base_action[0] += 40
        elif action == 'l':
            if s[0] > 40:
                base_action[0] -= 40

        self.canvas.move(self.rect, base_action[0], base_action[1])

        s_ = self.canvas.coords(self.rect)

        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
            s_ = 'terminal'
        elif s_ == self.canvas.coords(self.hell):
            reward = -1
            done = True
            s_ = 'terminal'
        else:
            reward = 0
            done = False

        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()

def update():
    for episode in range(100):
        observation = env.reset()
        while True:
            env.render()
            action = RL.choose_action(str(observation))
            observation_, reward, done = env.step(action)
            RL.learn(str(observation), action, reward, str(observation_))
            observation = observation_
            if done:
                break
    print("Game over!")
    env.destroy()

if __name__ == '__main__':
    env = Maze()
    RL = QLearningTable(actions=list(env.action_space))
    env.after(100, update)
    env.mainloop()