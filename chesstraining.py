import tkinter as tk
from tkinter import messagebox
from chess_logic import train_ai_parallel
from chess_ai import AI
from queue import Queue


class trainingapp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teaching App")
        self.num_games_var = tk.StringVar()
        self.num_processes_var = tk.StringVar(value="4")
        self.win_label = None
        self.draw_label = None
        self.loss_label = None
        self.setup_ui()

    def setup_ui(self):
        self.create_label("Number of Games:")
        self.create_entry(self.num_games_var)
        self.create_label("Number of Processes:")
        self.create_entry(self.num_processes_var)

        self.create_button("Train AI", self.start_training)

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

    def start_training(self):
        try:
            num_games = int(self.num_games_var.get())
            num_processes = int(self.num_processes_var.get())
        except ValueError:
            messagebox.showerror(
                "Error", "Invalid input. Please enter valid numbers.")
            return

        ai_with_knowledge = AI(epsilon=0.2)
        ai_without_knowledge = AI(epsilon=1.0)

        self.run_training(
            ai_with_knowledge, ai_without_knowledge, num_games, num_processes)

    def run_training(self, ai_with_knowledge, ai_without_knowledge, num_games, num_processes):
        wins = 0
        draws = 0
        losses = 0

        while wins + draws + losses < num_games:
            print(f"Training iteration {wins + draws + losses + 1}/{num_games}")
            batch_size = min(512, num_games - (wins + draws + losses))
            print(f"Batch size: {batch_size}")

            results_with_knowledge = train_ai_parallel(
                ai_with_knowledge, batch_size, num_processes)

            results_without_knowledge = train_ai_parallel(
                ai_without_knowledge, batch_size, num_processes)

            for result in results_with_knowledge:
                if result == 'win':
                    wins += 1
                elif result == 'draw':
                    draws += 1
                elif result == 'loss':
                    losses += 1

            for result in results_without_knowledge:
                if result == 'win':
                    wins += 1
                elif result == 'draw':
                    draws += 1
                elif result == 'loss':
                    losses += 1

            # Update labels
            self.update_counters(wins, draws, losses)

        messagebox.showinfo("Training Completed",
                            "AI training completed successfully.")

    def update_counters(self, wins, draws, losses):
        self.win_label.config(text=f"Wins: {wins}")
        self.draw_label.config(text=f"Draws: {draws}")
        self.loss_label.config(text=f"Losses: {losses}")


if __name__ == '__main__':
    root = tk.Tk()
    app = trainingapp(root)
