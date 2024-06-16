import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pyproj import Proj, Transformer

# Define projection systems
wgs84 = Proj('epsg:4326')  # WGS 84
ghana_nat_grid = Proj('epsg:2136')  # Ghana National Grid
ghana_meter_grid = Proj('epsg:25000')  # Example EPSG code for Ghana Meter Grid

class CoordinateTransformationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coordinate Transformation App")
        
        # Apply Cyberpunk theme styles
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a base theme to customize

        # Define colors for both themes
        self.dark_mode = {
            'background': '#0e0e0e',
            'current_line': '#1e1e1e',
            'foreground': '#00ff00',
            'button_bg': '#ffaf00'
        }

        self.bright_mode = {
            'background': '#ffffff',
            'current_line': '#f0f0f0',
            'foreground': '#000000',
            'button_bg': '#ffaf00'
        }

        self.current_theme = 'dark'

        self.apply_theme(self.dark_mode)  # Start with dark mode

        # Set up the user interface
        self.setup_ui()

        # Create menu
        self.create_menu()

    def apply_theme(self, theme):
        self.root.configure(bg=theme['background'])

        # Configure ttk styles
        self.style.configure('TLabel', background=theme['background'], foreground=theme['foreground'])
        self.style.configure('TEntry', fieldbackground=theme['current_line'], foreground=theme['foreground'])
        self.style.configure('TButton', background=theme['button_bg'], foreground=theme['foreground'])
        self.style.configure('TCombobox', fieldbackground=theme['current_line'], background=theme['current_line'], foreground=theme['foreground'])

    def setup_ui(self):
        # Input fields for coordinates
        self.input_label = ttk.Label(self.root, text="Input Coordinates:")
        self.input_label.grid(column=0, row=0, padx=10, pady=5)

        self.input_x_label = ttk.Label(self.root, text="X (Longitude):")
        self.input_x_label.grid(column=1, row=0, padx=10, pady=5)
        self.input_x = ttk.Entry(self.root)
        self.input_x.grid(column=2, row=0, padx=10, pady=5)

        self.input_y_label = ttk.Label(self.root, text="Y (Latitude):")
        self.input_y_label.grid(column=1, row=1, padx=10, pady=5)
        self.input_y = ttk.Entry(self.root)
        self.input_y.grid(column=2, row=1, padx=10, pady=5)

        # Dropdown for selecting transformation
        self.transformation_label = ttk.Label(self.root, text="Select Transformation:")
        self.transformation_label.grid(column=0, row=2, padx=10, pady=5)

        self.transformation = ttk.Combobox(self.root, values=[
            "WGS 84 to Ghana National Grid",
            "WGS 84 to Ghana Meter Grid",
            "Ghana National Grid to WGS 84",
            "Ghana Meter Grid to WGS 84"
        ])
        self.transformation.grid(column=1, row=2, padx=10, pady=5)
        self.transformation.current(0)  # Set default selection

        # Button to perform transformation
        self.transform_button = ttk.Button(self.root, text="Transform", command=self.transform_coordinates)
        self.transform_button.grid(column=2, row=2, padx=10, pady=5)

        # Button to save results
        self.save_button = ttk.Button(self.root, text="Save Result", command=self.save_result)
        self.save_button.grid(column=2, row=3, padx=10, pady=5)

        # Button to toggle theme
        self.toggle_theme_button = ttk.Button(self.root, text="Toggle Theme", command=self.toggle_theme)
        self.toggle_theme_button.grid(column=2, row=4, padx=10, pady=5)

        # Output fields for transformed coordinates
        self.output_label = ttk.Label(self.root, text="Output Coordinates:")
        self.output_label.grid(column=0, row=5, padx=10, pady=5)

        self.output_x_label = ttk.Label(self.root, text="X:")
        self.output_x_label.grid(column=1, row=5, padx=10, pady=5)
        self.output_x = ttk.Entry(self.root)
        self.output_x.grid(column=2, row=5, padx=10, pady=5)

        self.output_y_label = ttk.Label(self.root, text="Y:")
        self.output_y_label.grid(column=1, row=6, padx=10, pady=5)
        self.output_y = ttk.Entry(self.root)
        self.output_y.grid(column=2, row=6, padx=10, pady=5)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Create About menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def show_about(self):
        about_text = (
            "Coordinate Transformation App\n"
            "Version 1.0\n"
            "Created by Emmanuel Danso, a third-year Geomatic student.\n\n"
            "This application allows users to transform coordinates between different "
            "projection systems. Enter the coordinates, select the desired transformation, "
            "and click 'Transform' to see the results. You can also save the results to a text file."
        )
        messagebox.showinfo("About", about_text)

    def toggle_theme(self):
        if self.current_theme == 'dark':
            self.apply_theme(self.bright_mode)
            self.current_theme = 'bright'
        else:
            self.apply_theme(self.dark_mode)
            self.current_theme = 'dark'

    def transform_coordinates(self):
        # Validate input
        if not self.input_x.get() or not self.input_y.get():
            self.display_error("Please enter both coordinates.")
            return

        try:
            x = float(self.input_x.get())
            y = float(self.input_y.get())
        except ValueError:
            self.display_error("Invalid input. Please enter numeric values.")
            return

        # Get the selected transformation type from the combobox
        transformation_type = self.transformation.get()

        try:
            # Perform the appropriate transformation based on the selected type
            if transformation_type == "WGS 84 to Ghana National Grid":
                transformer = Transformer.from_proj(wgs84, ghana_nat_grid)
            elif transformation_type == "WGS 84 to Ghana Meter Grid":
                transformer = Transformer.from_proj(wgs84, ghana_meter_grid)
            elif transformation_type == "Ghana National Grid to WGS 84":
                transformer = Transformer.from_proj(ghana_nat_grid, wgs84)
            elif transformation_type == "Ghana Meter Grid to WGS 84":
                transformer = Transformer.from_proj(ghana_meter_grid, wgs84)
            else:
                self.display_error("Invalid transformation type selected.")
                return

            x2, y2 = transformer.transform(x, y)
            self.display_result(x2, y2)
        except Exception as e:
            self.display_error(str(e))

    def display_result(self, x2, y2):
        self.output_x.delete(0, tk.END)
        self.output_y.delete(0, tk.END)
        self.output_x.insert(0, f"{x2:.6f}")
        self.output_y.insert(0, f"{y2:.6f}")
        self.result = (x2, y2)

    def display_error(self, message):
        self.output_x.delete(0, tk.END)
        self.output_y.delete(0, tk.END)
        self.output_x.insert(0, "Error")
        self.output_y.insert(0, message)
        self.result = None

    def save_result(self):
        if not self.result:
            self.display_error("No valid result to save.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if save_path:
            with open(save_path, 'w') as file:
                file.write(f"Transformed Coordinates:\nX: {self.result[0]:.6f}\nY: {self.result[1]:.6f}")
            self.display_error("Result saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordinateTransformationApp(root)
    root.mainloop()