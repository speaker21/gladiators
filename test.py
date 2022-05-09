import tkinter as tk
root = tk.Tk()
root.geometry("400x240")

textExample=tk.Text(root, height=10)
textExample.pack()

textExample.configure(font=("Courier", 16, "italic"))

root.mainloop()