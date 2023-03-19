"""Class that rappresents a single node aka square"""
from pygame import draw,Color, Surface


class Square:
    def __init__(self, given_row, given_col,settings):
        self.settings = settings
        self.row = given_row
        self.col = given_col
        self.prerow = self.row-1
        self.nextrow = self.row+1
        self.nextcol = self.col+1
        self.precol = self.col-1
        self.width = self.settings.width_of_squares
        self.height = self.settings.height_of_squares
        self.total_rows = self.settings.rows
        self.total_columns = self.settings.columns
        self.x = given_row * self.width
        self.y = given_col * self.height
        self.color = self.settings.dead_color
        self.nextcolor= None
        self.neighbors = []

    # Checks if a square is in a given state

    def is_alive(self):
        return self.color == self.settings.alive_color

    def is_dead(self):
        return self.color == self.settings.dead_color

    # Sets a square in a given state

    def make_alive(self):
        self.color = self.settings.alive_color
 
    def make_dead(self):
        self.color = self.settings.dead_color
    
    def make_next_alive(self):
        self.nextcolor = self.settings.alive_color

    def make_next_dead(self):
        self.nextcolor = self.settings.dead_color

    def update(self):
        self.color = self.nextcolor

    def draw(self, window):
        draw.rect(window, (self.color),(self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        row = self.row
        col = self.col
        # Bottom
        if self.settings.pacman:
            nextrow = (self.nextrow+self.total_rows) % self.total_rows
            prerow = (self.prerow+self.total_rows) % self.total_rows
            nextcol = (self.nextcol+self.total_columns) % self.total_columns
            precol = (self.precol+self.total_columns) % self.total_columns

            if grid[nextrow][col].is_alive():
                self.neighbors.append(grid[nextrow][col]) #Bottom
            if grid[prerow][col].is_alive():
                self.neighbors.append(grid[prerow][col])#Top
            if grid[row][nextcol].is_alive():
                self.neighbors.append(grid[row][nextcol])#Right
            if grid[row][precol].is_alive():
                self.neighbors.append(grid[row][precol])#Left
            if grid[nextrow][precol].is_alive():
                self.neighbors.append(grid[nextrow][precol])#Bottom-left
            if grid[nextrow][nextcol].is_alive():
                self.neighbors.append(grid[nextrow][nextcol])#Bottom-right
            if grid[prerow][precol].is_alive():
                self.neighbors.append(grid[prerow][precol])#Top-left
            if grid[prerow][nextcol].is_alive():
                self.neighbors.append(grid[prerow][nextcol])#Top-right

        else:
            nextrow = self.nextrow
            prerow = self.prerow
            nextcol = self.nextcol
            precol = self.precol

            if row < self.total_rows-1 and grid[nextrow][col].is_alive(): # Bottom
                self.neighbors.append(grid[nextrow][col])

            if row > 0 and grid[prerow][col].is_alive():  # Top
                self.neighbors.append(grid[prerow][col])

            if col < self.total_columns-1 and grid[row][nextcol].is_alive(): # Right
                self.neighbors.append(grid[row][nextcol])

            if col > 0 and grid[row][precol].is_alive():  # Left
                self.neighbors.append(grid[row][precol])

            if row < self.total_rows-1 and col > 0 and grid[nextrow][precol].is_alive():  # Bottom-left 
                self.neighbors.append(grid[nextrow][precol])

            if row < self.total_rows-1 and col < self.total_columns-1 and grid[nextrow][nextcol].is_alive():  # Bottom-right
                self.neighbors.append(grid[nextrow][nextcol])

            if row > 0 and col > 0 and grid[prerow][precol].is_alive():  # Top-left
                self.neighbors.append(grid[prerow][precol])

            if row > 0 and col < self.total_columns-1 and grid[prerow][nextcol].is_alive():  # Top-right
                self.neighbors.append(grid[prerow][nextcol])
