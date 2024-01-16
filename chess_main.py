import tkinter as tk
from chessapp import chessapp
from Chess_ai import AI 
import tkinter

def show_startup_window():
    global show_instructions
    startup_root = tkinter.Tk()
    startup_root.title("Chess App")

    tkinter.Label(startup_root, text="Press mouse 3 for options").pack()

    var = tkinter.IntVar(value=1)

    def close_startup_window():
        global show_instructions
        show_instructions = var.get() == 1
        startup_root.destroy()

    tkinter.Button(startup_root, text="OK",
                   command=close_startup_window).pack()
    tkinter.Button(startup_root, text="Don't show again",
                   command=close_startup_window).pack()

    startup_root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Chess App")

    ai_instance = AI()

    app = chessapp(root, ai_instance)

    root.mainloop()
    