import tkinter as tk
from tkinter import messagebox

def show_fake_error(title, message):
    root = tk.Tk()
    root.withdraw()  
    root.attributes("-topmost", True)  
    
    messagebox.showerror(title, message)

    root.destroy()



