
    import tkinter as tk
    from tkinter import messagebox
    from Chess_ai import AI
    from chessapp import chessapp
    from chess_logic import train_ai_parallel, start_program

    if __name__ == "__main__":
        choice = messagebox.askquestion(
            "Chess App", "Do you want to train or open the GUI?")
        if choice == "yes":
            num_games = int(input("Enter the number of games to train the AI: "))
            num_processes = int(input("Enter the number of processes: "))
            ai_instance = AI()
            train_ai_parallel(ai_instance, num_games, num_processes)
        else:
            root = tk.Tk()
            root.title("Chess App")
            ai_instance = AI()
            app = ChessApp(root, ai_instance)
            root.mainloop()
