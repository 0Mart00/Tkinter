import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import json

class DraggableButtonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Draggable Button with Line Connection")
        self.root.geometry("800x600")

        self.buttons = []  # List to store the buttons
        self.lines = []    # List to store the lines
        self.selected_buttons = []  # List of selected buttons for drawing a line
        self.start_point = None  # The starting point for the line drawn with two clicks
        self.image = None  # Store image
        self.image_label = None  # Label for the image on the canvas

        # Create basic buttons
        self.new_label_button = tk.Button(root, text="New Label", command=self.add_draggable_button)
        self.new_label_button.place(x=10, y=10)

        self.line_button = tk.Button(root, text="Line", command=self.prepare_connection)
        self.line_button.place(x=110, y=10)

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.place(x=210, y=10)

        self.save_button = tk.Button(root, text="Save", command=self.save_to_file)
        self.save_button.place(x=310, y=10)

        self.load_from_file_button = tk.Button(root, text="Load", command=self.load_from_file)
        self.load_from_file_button.place(x=410, y=10)

        # Canvas for drawing lines and buttons
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        self.new_label_button.lift()  # Lift buttons above the canvas
        self.line_button.lift()
        self.load_button.lift()
        self.save_button.lift()
        self.load_from_file_button.lift()

        # Register click event for drawing a line with two clicks
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def add_draggable_button(self):
        # Ask user for the button name
        button_name = simpledialog.askstring("Button Name", "Enter button name:")
        if button_name:
            # Add a new button to the canvas
            btn = tk.Button(self.root, text=button_name)
            btn.place(x=100 + len(self.buttons) * 60, y=100)
            btn.bind("<Button-1>", self.start_drag)
            btn.bind("<B1-Motion>", self.on_drag)
            btn.bind("<Button-3>", self.select_button_for_connection)  # Right-click for selection

            self.buttons.append(btn)

    def start_drag(self, event):
        # Save initial positions for dragging
        self.start_x = event.x
        self.start_y = event.y
        self.current_button = event.widget

    def on_drag(self, event):
        # Calculate new position and place the button
        new_x = self.current_button.winfo_x() + (event.x - self.start_x)
        new_y = self.current_button.winfo_y() + (event.y - self.start_y)
        self.current_button.place(x=new_x, y=new_y)

        # Update lines if the button is connected to another
        self.update_lines()

    def prepare_connection(self):
        # Clear the selected buttons list for creating new connections
        self.selected_buttons = []
        print("Select two buttons for the connection! (Right-click to select)")

    def select_button_for_connection(self, event):
        # Add button to the selected list
        if len(self.selected_buttons) < 2:
            self.selected_buttons.append(event.widget)
            print(f"Selected button: {event.widget.cget('text')}")
        if len(self.selected_buttons) == 2:
            self.draw_line_between_buttons()

    def draw_line_between_buttons(self):
        # Draw a green line between two selected buttons
        btn1, btn2 = self.selected_buttons
        x1 = btn1.winfo_x() + btn1.winfo_width() // 2
        y1 = btn1.winfo_y() + btn1.winfo_height() // 2
        x2 = btn2.winfo_x() + btn2.winfo_width() // 2
        y2 = btn2.winfo_y() + btn2.winfo_height() // 2

        # Create the line and store it for later updates
        line = self.canvas.create_line(x1, y1, x2, y2, fill="green", width=2)
        self.lines.append((line, btn1, btn2))

    def update_lines(self):
        # Update the positions of the lines when a button is moved
        for line, btn1, btn2 in self.lines:
            x1 = btn1.winfo_x() + btn1.winfo_width() // 2
            y1 = btn1.winfo_y() + btn1.winfo_height() // 2
            x2 = btn2.winfo_x() + btn2.winfo_width() // 2
            y2 = btn2.winfo_y() + btn2.winfo_height() // 2
            self.canvas.coords(line, x1, y1, x2, y2)

    def on_canvas_click(self, event):
        # Draw a line between two clicks
        if self.start_point is None:
            self.start_point = (event.x, event.y)
        else:
            # Draw the line between the start and end points
            end_point = (event.x, event.y)
            self.canvas.create_line(self.start_point[0], self.start_point[1],
                                    end_point[0], end_point[1], fill="blue", width=2)
            self.start_point = None  # Reset the start point for the next line

    def load_image(self):
        # Load an image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((100, 100))  # Resize image to 100x100
            self.image = ImageTk.PhotoImage(image)

            if self.image_label:
                self.image_label.destroy()  # Remove existing image if there is one

            self.image_label = tk.Label(self.canvas, image=self.image)
            self.image_label.place(x=200, y=200)  # Initial position of the image
            self.image_label.bind("<Button-1>", self.start_drag_image)
            self.image_label.bind("<B1-Motion>", self.on_drag_image)

    def start_drag_image(self, event):
        # Save initial positions for dragging the image
        self.start_x = event.x
        self.start_y = event.y
        self.current_image = event.widget

    def on_drag_image(self, event):
        # Calculate new position and place the image
        new_x = self.current_image.winfo_x() + (event.x - self.start_x)
        new_y = self.current_image.winfo_y() + (event.y - self.start_y)
        self.current_image.place(x=new_x, y=new_y)

    def save_to_file(self):
        # Save data to file
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            data = {
                'buttons': [{'x': btn.winfo_x(), 'y': btn.winfo_y(), 'text': btn.cget('text')} for btn in self.buttons],
                'lines': [{'x1': line[1].winfo_x() + line[1].winfo_width() // 2, 'y1': line[1].winfo_y() + line[1].winfo_height() // 2,
                           'x2': line[2].winfo_x() + line[2].winfo_width() // 2, 'y2': line[2].winfo_y() + line[2].winfo_height() // 2}
                          for line in self.lines],
                'image': {'x': self.image_label.winfo_x(), 'y': self.image_label.winfo_y()} if self.image_label else None
            }
            with open(file_path, "w") as f:
                json.dump(data, f)
            print("Data saved!")

    def load_from_file(self):
        # Load data from file
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    print("Data loaded!")

                    # Recreate buttons
                    for btn_data in data['buttons']:
                        btn = tk.Button(self.root, text=btn_data['text'])
                        btn.place(x=btn_data['x'], y=btn_data['y'])
                        btn.bind("<Button-1>", self.start_drag)
                        btn.bind("<B1-Motion>", self.on_drag)
                        btn.bind("<Button-3>", self.select_button_for_connection)
                        self.buttons.append(btn)

                    # Redraw lines
                    for line_data in data['lines']:
                        self.canvas.create_line(line_data['x1'], line_data['y1'],
                                                line_data['x2'], line_data['y2'], fill="green", width=2)

                    # Load image
                    if data['image']:
                        self.image_label.place(x=data['image']['x'], y=data['image']['y'])

            except FileNotFoundError:
                print("File not found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DraggableButtonApp(root)
    root.mainloop()
