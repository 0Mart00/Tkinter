import tkinter as tk
from tkinter import filedialog, messagebox

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            text_content = text_area.get("1.0", "end-1c")
            file.write(text_content)
        messagebox.showinfo("Information", "File saved successfully.")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", file.read())

def clear_text():
    text_area.delete("1.0", tk.END)

def about():
    messagebox.showinfo("About", "Simple Text Editor\nCreated using Tkinter")

# Create the main application window
root = tk.Tk()
root.title("Simple Text Editor")

# Create a text area
text_area = tk.Text(root, wrap="word")
text_area.pack(expand=True, fill="both")

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Clear", command=clear_text)

# Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about)

# Run the application
root.mainloop()
