import tkinter as tk
import random

# Constants to represent cell states
GREEN = 0
RED = 1
GREY = 2
WHITE = 3

class ForestFireSimulation:
    def __init__(self, width, height, density, start_fire_x, start_fire_y):
        self.width = width
        self.height = height
        self.grid = [[GREEN if random.random() < density else WHITE for _ in range(width)] for _ in range(height)]  # Initialize grid with trees or empty space
        self.grid[start_fire_y][start_fire_x] = RED  # Start fire at specified cell
        self.density = density

    def update(self):
        new_grid = [[cell for cell in row] for row in self.grid]   

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == GREEN:
                    if self.has_nearby_fire(x, y):
                        new_grid[y][x] = RED
                elif self.grid[y][x] == RED:
                    new_grid[y][x] = GREY
                elif self.grid[y][x] == GREY:
                    new_grid[y][x] = WHITE

        # Update grid
        self.grid = new_grid

    def has_nearby_fire(self, x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[ny][nx] == RED:
                return True
        return False

class ForestFireGUI:
    def __init__(self, master):
        self.master = master
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.density_var = tk.StringVar()
        self.start_x_var = tk.StringVar()
        self.start_y_var = tk.StringVar()

        self.create_input_widgets()

    def create_input_widgets(self):
        tk.Label(self.master, text="Width:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.master, textvariable=self.width_var, font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(self.master, text="Height:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.master, textvariable=self.height_var, font=("Arial", 14)).grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(self.master, text="Density:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.master, textvariable=self.density_var, font=("Arial", 14)).grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(self.master, text="Start X:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.master, textvariable=self.start_x_var, font=("Arial", 14)).grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(self.master, text="Start Y:", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=10)
        tk.Entry(self.master, textvariable=self.start_y_var, font=("Arial", 14)).grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        tk.Button(self.master, text="Run Simulation", font=("Arial", 14), command=self.run_simulation).grid(row=5, column=0, columnspan=2, pady=20)

        # Set column and row weights
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)
        self.master.rowconfigure(3, weight=1)
        self.master.rowconfigure(4, weight=1)
        self.master.rowconfigure(5, weight=1)

    def run_simulation(self):
        width = int(self.width_var.get())
        height = int(self.height_var.get())
        density = float(self.density_var.get())
        start_x = int(self.start_x_var.get())
        start_y = int(self.start_y_var.get())

        root = tk.Tk()
        root.title("Forest Fire Simulation")

        gui = ForestFireSimulationGUI(root, width, height, density, start_x, start_y)

        root.mainloop()

class ForestFireSimulationGUI:
    def __init__(self, master, width, height, density, start_fire_x, start_fire_y):
        self.master = master
        self.width = width
        self.height = height
        self.simulation = ForestFireSimulation(width, height, density, start_fire_x, start_fire_y)

        # Increase canvas size by multiplying with a scaling factor
        canvas_width = width * 15
        canvas_height = height * 15

        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height, bg='white')
        self.canvas.pack()

        self.update()

    def update(self):
        self.simulation.update()
        self.draw()
        self.master.after(2000, self.update)

    def draw(self):
        self.canvas.delete('all')
        for y in range(self.height):
            for x in range(self.width):
                color = 'green' if self.simulation.grid[y][x] == GREEN else \
                        'red' if self.simulation.grid[y][x] == RED else \
                        'grey' if self.simulation.grid[y][x] == GREY else \
                        'white'
                self.canvas.create_rectangle(x * 15, y * 15, (x + 1) * 15, (y + 1) * 15, fill=color)

def main():
    root = tk.Tk()
    root.title("Forest Fire Simulation")
    app = ForestFireGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
