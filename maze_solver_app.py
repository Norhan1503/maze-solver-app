import tkinter as tk
from tkinter import filedialog, messagebox
import searching_algorithms

class MazeSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")
        self.root.geometry("900x700")
        self.root.config(bg="#2c3e50")
        
        # Maze variables
        self.maze_data = None
        self.start_symbol = None
        self.end_symbol = None
        self.start = None
        self.end = None
        self.path_items = []  # List to keep track of drawn path items
        
        # Setup GUI components
        self.setup_gui()

    def setup_gui(self):
        # Frame for options
        options_frame = tk.Frame(self.root, bg="#34495e", bd=2, relief=tk.RIDGE)
        options_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Enter maze button
        enter_maze_button = tk.Button(options_frame, text="Enter Maze as text file", command=self.load_maze, font=("Arial", 12, "bold"),
                                      bg="#1abc9c", fg="white", relief=tk.GROOVE, activebackground="#16a085")
        enter_maze_button.pack(pady=20, ipadx=10, ipady=5)
        
        # Text boxes for start and end symbols
        start_label = tk.Label(options_frame, text="Start Symbol (A):", font=("Arial", 12, "bold"), bg="#34495e", fg="white")
        start_label.pack(pady=5)
        self.start_entry = tk.Entry(options_frame, font=("Arial", 12))
        self.start_entry.insert(0, "A")
        self.start_entry.pack(pady=5)

        end_label = tk.Label(options_frame, text="End Symbol (B):", font=("Arial", 12, "bold"), bg="#34495e", fg="white")
        end_label.pack(pady=5)
        self.end_entry = tk.Entry(options_frame, font=("Arial", 12))
        self.end_entry.insert(0, "B")
        self.end_entry.pack(pady=5)
        
        # Algorithm selection
        self.algo_var = tk.StringVar(value="")
        algo_label = tk.Label(options_frame, text="Select Algorithm:", font=("Arial", 14, "bold"),
                              bg="#34495e", fg="white")
        algo_label.pack(pady=10)

        for algo in ["BFS", "DFS", "A*", "Genetic Algorithm"]:
            algo_button = tk.Radiobutton(options_frame, text=algo, variable=self.algo_var, value=algo,
                                         font=("Arial", 12), bg="#34495e", fg="white", selectcolor="#16a085",
                                         activebackground="#16a085", anchor="w", command=self.on_algo_select)
            algo_button.pack(anchor="w", padx=20)
        
        # Solve button
        self.solve_button = tk.Button(options_frame, text="Solve Maze", command=self.solve_maze, font=("Arial", 12, "bold"),
                                      bg="#e74c3c", fg="white", relief=tk.GROOVE, activebackground="#c0392b")
        self.solve_button.pack(pady=40, ipadx=10, ipady=5)
        self.solve_button.config(state="disabled")
        
        # Canvas for maze display
        self.canvas_frame = tk.Frame(self.root, bg="#ecf0f1", bd=2, relief=tk.SUNKEN)
        self.canvas_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=600, height=600, bg="white")
        self.canvas.pack(expand=True, fill="both", padx=10, pady=10)

    def on_algo_select(self):
        if self.algo_var.get():
            self.solve_button.config(state="normal")
        else:
            self.solve_button.config(state="disabled")

    def load_maze(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not filepath:
            return

        self.start_symbol = self.start_entry.get().strip()
        self.end_symbol = self.end_entry.get().strip()

        if len(self.start_symbol) != 1 or len(self.end_symbol) != 1:
            messagebox.showerror("Error", "Start and end symbols must be a single character each.")
            return

        with open(filepath, 'r') as file:
            lines = file.readlines()
        
        self.maze_data = []
        self.start = None
        self.end = None

        for i, line in enumerate(lines):
            row = []
            for j, ch in enumerate(line):  # line.strip()
                if ch == self.start_symbol:
                    self.start = (i, j)
                    row.append(0)
                elif ch == self.end_symbol:
                    self.end = (i, j)
                    row.append(0)
                else:
                    row.append(0 if ch == ' ' else 1)
            self.maze_data.append(row)
        
        if self.start is None or self.end is None:
            messagebox.showerror("Error", f"Maze must contain both start ('{self.start_symbol}') and end ('{self.end_symbol}') points.")
            return

        self.display_maze()
        self.filepath = filepath

    def display_maze(self):
        self.canvas.delete("all")
        if not self.maze_data:
            return
        
        rows = len(self.maze_data)
        cols = len(self.maze_data[0])
        
        cell_width = 600 // cols
        cell_height = 600 // rows
        
        for i, row in enumerate(self.maze_data):
            for j, cell in enumerate(row):
                color = "black" if cell == 1 else "white"
                if (i, j) == self.start:
                    color = "green"
                elif (i, j) == self.end:
                    color = "blue"
                self.canvas.create_rectangle(j * cell_width, i * cell_height,
                                             (j + 1) * cell_width, (i + 1) * cell_height,
                                             fill=color, outline="grey")

    def solve_maze(self):
        algorithm = self.algo_var.get()
        if not self.maze_data:
            messagebox.showerror("Error", "Please load a maze first.")
            return
        

        maze, error = searching_algorithms.Maze.create(self.filepath, self.start_entry.get(), self.end_entry.get())
        if error:
            messagebox.showerror("Maze Error", error)
            return
        
        if self.path_items:
            # Clear the old path
            for item in self.path_items:
                self.canvas.delete(item)
            self.path_items.clear()
    
        if algorithm in searching_algorithms.algorithms:
            try:
                path = maze.solve(algorithm)
                if path is not None:
                    self.display_path(path)
                else:
                    messagebox.showinfo("No Solution", "No path found from start to end.")
            except Exception as e:
                messagebox.showerror("Solving Error", f"An error occurred while solving the maze: {str(e)}")
    
    def display_path(self, path):
        """Display the path on the canvas."""
        if not self.maze_data:
            return
        
        rows = len(self.maze_data)
        cols = len(self.maze_data[0])
        
        cell_width = 600 // cols
        cell_height = 600 // rows
        
        for (x, y) in path:
            item = self.canvas.create_oval(y * cell_width + cell_width // 4, x * cell_height + cell_height // 4,
                                           y * cell_width + 3 * cell_width // 4, x * cell_height + 3 * cell_height // 4,
                                           fill="red", outline="red")
            start_x, start_y = self.start
            self.canvas.create_oval(start_y * cell_width + cell_width // 4, start_x * cell_height + cell_height // 4,
                            start_y * cell_width + 3 * cell_width // 4, start_x * cell_height + 3 * cell_height // 4,
                            fill="red", outline="red")
            self.path_items.append(item)  # Store the item to delete later


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolverApp(root)
    root.mainloop()
