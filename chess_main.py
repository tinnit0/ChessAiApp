import tkinter as tk
from chessapp import chessapp
from chess_ai import AI

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Chess App")

    ai_instance = AI()

    app = chessapp(root, ai_instance)

    root.mainloop()