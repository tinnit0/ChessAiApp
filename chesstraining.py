import tkinter as tk
from tkinter import messagebox
from chess_logic import Logic
from Chess_ai import AI

class TrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teaching App")
        self.num_games_var = tk.StringVar()
        self.num_processes_var = tk.StringVar(value="4")
        self.win_label = None
        self.draw_label = None
        self.loss_label = None
        self.text_areas = []
        self.logic_instance = Logic()
        self.ai_with_knowledge = AI(epsilon=0.2)
        self.ai_without_knowledge = AI(epsilon=1.0)
        self.training_mode = False
        self.setup_ui()
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def setup_ui(self):
        self.create_label("Number of Games:")
        self.create_entry(self.num_games_var)
        self.create_label("Number of Processes:")
        self.create_entry(self.num_processes_var)

        train_button = tk.Button(self.root, text="Train AI", command=self.start_training)
        train_button.pack(pady=20)
 
        self.win_label = tk.Label(self.root, text="Wins: 0")
        self.win_label.pack(pady=5)     

        self.draw_label = tk.Label(self.root, text="Draws: 0")
        self.draw_label.pack(pady=5)

        self.loss_label = tk.Label(self.root, text="Losses: 0")
        self.loss_label.pack(pady=5)

        self.root.mainloop()

    def create_label(self, text):
        tk.Label(self.root, text=text).pack(pady=10)   

    def create_entry(self, variable):
        tk.Entry(self.root, textvariable=variable).pack(pady=10)
        
    def create_button(self, text, command):
        tk.Button(self.root, text=text, command=command).pack(pady=20)

    def run_training(self, num_games, num_processes):
        wins = 0
        draws = 0
        losses = 0

        current_iteration = 0
        max_iterations = num_games // 512  # Adjust as needed

        def training_iteration():
            nonlocal wins, draws, losses, current_iteration

            if current_iteration < max_iterations:
                print(f"Training iteration {current_iteration + 1}/{max_iterations}")
                batch_size = min(512, num_games - (current_iteration * 512))
                print(f"Batch size: {batch_size}")

                results_with_knowledge = self.logic_instance.train_ai_parallel(
                    self.ai_with_knowledge, batch_size, num_processes
                )

                results_without_knowledge = self.logic_instance.train_ai_parallel(
                    self.ai_without_knowledge, batch_size, num_processes
                )

                self.update_counters(wins, draws, losses)

                current_iteration += 1
                self.root.after(1, training_iteration)
            else:
                messagebox.showinfo("Training Completed", "AI training completed successfully.")

        training_iteration()

    def play_against_ai(self):
        self.training_mode = False

    def start_training(self):
        self.training_mode = True
        try:
            num_games = int(self.num_games_var.get())
            num_processes = int(self.num_processes_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")
            return

        self.run_training(num_games, num_processes)

    def update_counters(self, wins, draws, losses):
        self.win_label.config(text=f"Wins: {wins}")
        self.draw_label.config(text=f"Draws: {draws}")
        self.loss_label.config(text=f"Losses: {losses}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingApp(root)
    root.mainloop()