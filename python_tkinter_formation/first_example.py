import tkinter as tk
from tkinter import ttk


class FeetToMeters(ttk.Frame):
    def __init__(self, master: tk.Misc | None = None, *args, **kwargs) -> None:
        ttk.Frame.__init__(self, master, *args, **kwargs)
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.feet = tk.StringVar()
        self.feet_entry = ttk.Entry(
            self, width=7, textvariable=self.feet, justify="right"
        )
        self.feet_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

        self.meters = tk.StringVar()
        ttk.Label(self, textvariable=self.meters, anchor=tk.E).grid(
            column=2, row=2, sticky=(tk.W, tk.E)
        )

        ttk.Label(self, text="feet").grid(column=3, row=1, sticky=tk.W)
        ttk.Label(self, text="is equivalent to").grid(
            column=1, row=2, sticky=tk.E
        )
        ttk.Label(self, text="meters").grid(column=3, row=2, sticky=tk.W)

        ttk.Button(self, text="Calculate", command=self.calculate).grid(
            column=3, row=3, sticky=tk.W
        )

        # Set padding around each child
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.feet_entry.focus()

        # self.feet.trace_add('write', self.calculate)
        self.master.bind("<Return>", self.calculate)

    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(f"{0.3048 * value:.2f}")
        except ValueError:
            pass
