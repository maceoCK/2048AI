import tkinter as tk
import colors as c
import random


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.master.resizable(False, False)
        self.main_grid = tk.Frame(
            self, bg=c.GRID_COLOR, bd=3, width=600, height=600
        )
        self.high_score = 0
        self.main_grid.grid(pady=(100, 0))
        self.makeGUI()
        self.start_game()
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()

    def take_action(self, action):
        if action == "left":
            self.left(None)
        elif action == "right":
            self.right(None)
        elif action == "up":
            self.up(None)
        elif action == "down":
            self.down(None)
        else:
            raise ValueError(f"Invalid action: {action}")

    def makeGUI(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=150,
                    height=150
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)
        
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.17, y=45, anchor="center")

        high_score_frame = tk.Frame(self)
        high_score_frame.place(relx=0.75, y=45, anchor="center")
        tk.Label(
            score_frame,
            text="Score",
            font=c.SCORE_LABEL_FONT
        ).grid(row=0)
        tk.Label(
            high_score_frame,
            text="High Score",
            font=c.SCORE_LABEL_FONT
        ).grid(row=0)
        self.high_score_label = tk.Label(high_score_frame, text=str(self.high_score), font=c.SCORE_FONT)
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)
        self.high_score_label.grid(row=1)

    def start_game(self):
        self.matrix = [[0] * 4 for _ in range(4)]

        row = random.randint(0, 3)
        col = random.randint(0, 3)

        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2"
        )
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2"
        )
        self.score = 0
    
    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix
    
    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    self.score += self.matrix[i][j]
    
    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3-j])
        self.matrix = new_matrix
    
    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix
    
    def add_new_tile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 4])
    
    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(
                        bg=c.EMPTY_CELL_COLOR,
                        text=""
                    )
                else:
                    self.cells[i][j]["frame"].configure(
                        bg=c.CELL_COLORS[cell_value]
                    )
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[cell_value],
                        fg=c.CELL_NUMBER_COLORS[cell_value],
                        font=c.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value)
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def left(self, event):
        if self.check_if_can_move("left"):
            self.stack()
            self.combine()
            self.stack()
            self.add_new_tile()
            self.update_GUI()
            self.game_over()
            
    
    def right(self, event):
        if self.check_if_can_move("right"):
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
            self.add_new_tile()
            self.update_GUI()
            self.game_over()

    
    def up(self, event):
        if self.check_if_can_move("up"):
            self.transpose()
            self.stack()
            self.combine()
            self.stack()
            self.transpose()
            self.add_new_tile()
            self.update_GUI()
            self.game_over()
    
    def down(self, event):
        if self.check_if_can_move("down"):
            self.transpose()
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
            self.transpose()
            self.add_new_tile()
            self.update_GUI()
            self.game_over()
    

    def check_if_can_move(self, direction):
        if direction == "up":
            for i in range(1, 4):
                for j in range(4):
                    if self.matrix[i][j] != 0 and (self.matrix[i-1][j] == 0 or self.matrix[i][j] == self.matrix[i-1][j]):
                        return True
            return False
        elif direction == "down":
            for i in range(3):
                for j in range(4):
                    if self.matrix[i][j] != 0 and (self.matrix[i+1][j] == 0 or self.matrix[i][j] == self.matrix[i+1][j]):
                        return True
            return False
        elif direction == "left":
            for i in range(4):
                for j in range(1, 4):
                    if self.matrix[i][j] != 0 and (self.matrix[i][j-1] == 0 or self.matrix[i][j] == self.matrix[i][j-1]):
                        return True
            return False
        elif direction == "right":
            for i in range(4):
                for j in range(3):
                    if self.matrix[i][j] != 0 and (self.matrix[i][j+1] == 0 or self.matrix[i][j] == self.matrix[i][j+1]):
                        return True
            return False

    def reset(self):
        self.main_grid.destroy()
        self.grid()
        self.main_grid = tk.Frame(
            self, bg=c.GRID_COLOR, bd=3, width=600, height=600
        )
        self.main_grid.grid(pady=(100, 0))
        self.makeGUI()
        self.start_game()

    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False
    
    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False
    
    def game_over(self):
        if any(2048 in row for row in self.matrix):
            self.show_game_over_message("You win!", c.WINNER_BG)
            self.create_restart_button()
            return True
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            self.show_game_over_message("Game over!", c.LOSER_BG)
            self.create_restart_button()
            return True
        return False

    def show_game_over_message(self, message, bg_color):
        game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        if (self.score > self.high_score):
            self.high_score = self.score
        self.high_score_label.configure(text=str(self.high_score))
        tk.Label(
            game_over_frame,
            text=message,
            bg=bg_color,
            fg=c.GAME_OVER_FONT_COLOR,
            font=c.GAME_OVER_FONT
        ).pack()

    def create_restart_button(self):
        restart_button = tk.Button(
            self.main_grid,
            text="Play Again",
            command=self.restart_game,
            bg=c.WINNER_BG,
            fg="#000000",
            font=c.GAME_OVER_FONT
        )
        restart_button.grid(row=5, column=0, columnspan=4)

    def restart_game(self):
        self.reset()

if __name__ == "__main__":
    playing = True
    game = Game()
    

            
