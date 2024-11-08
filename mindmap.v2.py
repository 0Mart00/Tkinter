import tkinter as tk
from tkinter import colorchooser, filedialog
import json
import os

class ButtonMover:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomb Mozgató és Vonalkészítő")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.buttons = []  # Lista a gombok tárolására
        self.button_objects = []  # Lista a gomb objektumok tárolására
        self.drag_data = {"x": 0, "y": 0, "button": None}  # Mozgatás adat
        self.lines = []  # Vonalként tárolt koordináták
        self.line = None  # Az aktuális vonal
        self.start_point = None  # A vonal kezdőpontja
        self.line_color = "#000000"  # Alapértelmezett vonalszín (fekete)

        # Gomb hozzáadása a vászonra
        self.add_button = tk.Button(root, text="Gomb hozzáadása", command=self.add_button_to_canvas)
        self.add_button.pack()

        # Színválasztás gomb
        self.color_button = tk.Button(root, text="Vonal szín választása", command=self.choose_line_color)
        self.color_button.pack()

        # Vonalképzés
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        # Betöltés vagy új fájl kiválasztása
        self.file_path = self.choose_file()
        if self.file_path:
            self.load_data(self.file_path)  # Ha van fájl, betöltjük

    def choose_file(self):
        # Fájl kiválasztás dialógus
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if not file_path:
            # Ha nincs választva fájl, új fájlt választunk ki mentéshez
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        return file_path

    def add_button_to_canvas(self):
        # Új gombot adunk hozzá a vászonhoz egy véletlenszerű helyre
        x, y = 100, 100  # Kezdő pozíció
        button = tk.Button(self.root, text=f"Gomb {len(self.buttons) + 1}", command=lambda: self.on_button_click(len(self.buttons)))
        button.place(x=x, y=y)
        self.buttons.append((x, y))  # Gomb pozíció tárolása
        self.button_objects.append(button)  # Gomb objektum tárolása
        self.save_data()  # Mentés

        # A gomb mozgatásának eseményei
        button.bind("<ButtonPress-1>", self.on_button_press)
        button.bind("<B1-Motion>", self.on_button_drag)
        button.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_click(self, button_index):
        # Esemény, amikor a gombra kattintunk
        print(f"Gomb {button_index + 1} lett megnyomva.")

    def on_button_press(self, event):
        # Kezdő pozíció tárolása, amikor a gombra kattintunk
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["button"] = event.widget

    def on_button_drag(self, event):
        # Mozgatás közben a gomb pozíciójának frissítése
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        
        # Új pozíció kiszámítása
        new_x = self.drag_data["button"].winfo_x() + dx
        new_y = self.drag_data["button"].winfo_y() + dy
        
        # A gomb új helye
        self.drag_data["button"].place(x=new_x, y=new_y)

        # A pozíció frissítése a tárolt adatokban
        button_index = self.button_objects.index(self.drag_data["button"])
        self.buttons[button_index] = (new_x, new_y)
        
        # Mentés a gombok új pozícióval
        self.save_data()

    def on_button_release(self, event):
        # Mozgatás befejezése
        self.drag_data["button"] = None

    def on_canvas_click(self, event):
        # Kattintás a vásznon (vonal kezdőpontja)
        if self.start_point is None:
            self.start_point = (event.x, event.y)
        else:
            self.line = self.canvas.create_line(self.start_point[0], self.start_point[1], event.x, event.y, fill=self.line_color)
            self.lines.append((self.start_point, (event.x, event.y)))  # Tároljuk a vonalat
            self.start_point = None  # Vonal végződése

        self.save_data()  # Mentés

    def on_canvas_drag(self, event):
        # Ha van éppen húzott vonal, folytatjuk a rajzolást
        if self.line:
            self.canvas.coords(self.line, self.start_point[0], self.start_point[1], event.x, event.y)

    def on_canvas_release(self, event):
        # Vonal befejezése
        self.line = None

    def choose_line_color(self):
        # Színválasztó párbeszédablak megnyitása
        color = colorchooser.askcolor()[1]  # A színkódot kapjuk vissza
        if color:
            self.line_color = color  # Beállítjuk az új vonalszínt

    def save_data(self):
        # A gombok és vonalak pozícióját mentjük el
        data = {
            "buttons": self.buttons,
            "lines": self.lines
        }
        if self.file_path:  # Ha van érvényes fájl útvonal
            with open(self.file_path, "w") as f:
                json.dump(data, f)

    def load_data(self, file_path):
        # Gombok és vonalak betöltése a fájlból, ha létezik
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
            
            # Gombok kirajzolása a betöltött pozíciók alapján
            for i, (x, y) in enumerate(data["buttons"]):
                button = tk.Button(self.root, text=f"Gomb {i + 1}", command=lambda i=i: self.on_button_click(i))
                button.place(x=x, y=y)
                self.button_objects.append(button)  # Hozzáadjuk a gomb objektumot a listához

                # A gomb mozgatásának eseményei
                button.bind("<ButtonPress-1>", self.on_button_press)
                button.bind("<B1-Motion>", self.on_button_drag)
                button.bind("<ButtonRelease-1>", self.on_button_release)

            # Vonalak kirajzolása
            for line_start, line_end in data["lines"]:
                self.canvas.create_line(line_start[0], line_start[1], line_end[0], line_end[1], fill=self.line_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = ButtonMover(root)
    root.mainloop()
