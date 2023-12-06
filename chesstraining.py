import tkinter as tk
from tkinter import ttk, messagebox
from chess_logic import train_ai_parallel
from chess_ai import AI
import threading
from queue import Queue


class trainingapp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teaching App")
        self.num_games_var = tk.StringVar()
        self.num_processes_var = tk.StringVar(value="4")
        self.progressbars = []
        self.progress_queue = Queue()
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Number of Games:").pack(pady=10)
        tk.Entry(self.root, textvariable=self.num_games_var).pack(pady=10)
        tk.Label(self.root, text="Number of Processes:").pack(pady=10)
        tk.Entry(self.root, textvariable=self.num_processes_var).pack(pady=10)

        tk.Button(self.root, text="Train AI",
                  command=self.start_training).pack(pady=20)

    def start_training(self):
        try:
            num_games = int(self.num_games_var.get())
            num_processes = int(self.num_processes_var.get())
        except ValueError:
            messagebox.showerror(
                "Error", "Invalid input. Please enter valid numbers.")
            return

        threading.Thread(target=self.run_training, args=(
            num_games, num_processes)).start()

    def create_progress_bars(self, num_processes):
        for i in range(num_processes):
            progress_label = tk.Label(self.root, text=f"Process {i + 1}")
            progress_label.pack(pady=5)
            progressbar = ttk.Progressbar(
                self.root, orient="horizontal", length=200, mode="indeterminate"
            )
            progressbar.pack(pady=5)
            self.progressbars.append((progress_label, progressbar))

    def update_progress(self, process_index, message, value):
        label, progressbar = self.progressbars[process_index]
        label.config(text=f"Process {process_index + 1}: {message}")
        progressbar.step(value)
        self.root.update_idletasks()

    def run_training(self, num_games, num_processes):
        ai_instance = AI()
        self.create_progress_bars(num_processes)
        results = train_ai_parallel(
            ai_instance, num_games, num_processes, self.progress_queue)
        messagebox.showinfo("Training Completed",
                            "AI training completed successfully.")
        self.progressbars = []


if __name__ == '__main__':
    root = tk.Tk()
    app = trainingapp(root)
    root.mainloop()
