import tkinter as tk
from bouncing import BouncingCanvas

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bouncing balls")
    root.geometry("500x500")
    BouncingCanvas(root, bg="black", width=850, height=400)
    root.mainloop()
