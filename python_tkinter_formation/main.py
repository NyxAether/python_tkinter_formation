import tkinter as tk

# from first_example import FeetToMeters
from python_tkinter_formation.bouncing import BouncingCanvas

if __name__ == "__main__":
    root = tk.Tk()
    # root.title('Feet to Meters')
    # FeetToMeters(root, padding="3 3 12 12")
    root.title("Bouncing balls")
    root.geometry("500x500")
    BouncingCanvas(root, bg="black", width=850, height=400)
    root.mainloop()
