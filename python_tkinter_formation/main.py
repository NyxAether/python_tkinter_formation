import tkinter as tk
from first_example import FeetToMeters

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Feet to Meters")
    FeetToMeters(root, padding="3 3 12 12")
    root.mainloop()
