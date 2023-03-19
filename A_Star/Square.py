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
        self.color = self.settings.bg_color
        self.neighbors = []
    # Checks if a square is in a given state

    def get_pos(self):
        return self.row, self.col  # Return y ,x

    def is_closed(self):
        return self.color == self.settings.closed_color

    def is_open(self):
        return self.color == self.settings.open_color

    def is_barrier(self):
        return self.color == self.settings.barrier_color

    def is_start(self):
        return self.color == self.settings.start_color

    def is_end(self):
        return self.color == self.settings.end_color

    def is_path(self):
        return self.color == self.settings.path_color

    def is_bg(self):
        return self.color == self.settings.bg_color

    # Sets a square in a given state

    def make_closed(self):
        self.color = self.settings.closed_color

    def make_open(self):
        self.color = self.settings.open_color

    def make_barrier(self):
        self.color = self.settings.barrier_color

    def make_start(self):
        self.color = self.settings.start_color

    def make_end(self):
        self.color = self.settings.end_color

    def make_path(self):
        self.color = self.settings.path_color
 
    def make_bg(self):
        self.color = self.settings.bg_color

    def draw(self, window):
        draw.rect(window, self.color,
                  (self.x, self.y, self.width, self.height))

    def update_neighbors(self, grid):
        if self.is_barrier():
            return
        row = self.row
        col = self.col
        # Bottom
        if self.settings.pacman:
            nextrow = (self.nextrow+self.total_rows) % self.total_rows
            prerow = (self.prerow+self.total_rows) % self.total_rows
            nextcol = (self.nextcol+self.total_columns) % self.total_columns
            precol = (self.precol+self.total_columns) % self.total_columns
            if not grid[nextrow][col].is_barrier():
                self.neighbors.append(grid[nextrow][col])

            if not grid[prerow][col].is_barrier():  # Top
                self.neighbors.append(grid[prerow][col])

            # Right
            if not grid[row][nextcol].is_barrier():
                self.neighbors.append(grid[row][nextcol])

            if not grid[row][precol].is_barrier():  # Left
                self.neighbors.append(grid[row][precol])

            if self.settings.diagonals and self.settings.consider_barrier == False:
                # Bottom-left
                if not grid[nextrow][precol].is_barrier():
                    self.neighbors.append(grid[nextrow][precol])

                # Bottom-right
                if not grid[nextrow][nextcol].is_barrier():
                    self.neighbors.append(grid[nextrow][nextcol])

                # Top-left
                if not grid[prerow][precol].is_barrier():
                    self.neighbors.append(grid[prerow][precol])

                # Top-right
                if not grid[prerow][nextcol].is_barrier():
                    self.neighbors.append(grid[prerow][nextcol])

            elif self.settings.diagonals and self.settings.consider_barrier:
                if not grid[nextrow][precol].is_barrier() and not grid[row][precol].is_barrier() \
                        and not grid[nextrow][col].is_barrier():  # Bottom-left and left and bottom are not barriers
                    self.neighbors.append(grid[nextrow][precol])

                if not grid[nextrow][nextcol].is_barrier() and not grid[row][nextcol].is_barrier() \
                        and not grid[nextrow][col].is_barrier():  # Bottom-right and right and bottom are not barriers
                    self.neighbors.append(grid[nextrow][nextcol])

                if not grid[prerow][precol].is_barrier() and not grid[row][precol].is_barrier()\
                        and not grid[prerow][col].is_barrier():  # Top-left and left and top are not barriers
                    self.neighbors.append(grid[prerow][precol])

                if not grid[prerow][nextcol].is_barrier() and not grid[row][nextcol].is_barrier()\
                        and not grid[prerow][col].is_barrier():  # Top-right and right and top are not barriers
                    self.neighbors.append(grid[prerow][nextcol])
        else:
            nextrow = self.nextrow
            prerow = self.prerow
            nextcol = self.nextcol
            precol = self.precol

            if row < self.total_rows-1 and not grid[nextrow][col].is_barrier():#Bottom
                self.neighbors.append(grid[nextrow][col])

            if row > 0 and not grid[prerow][col].is_barrier():  # Top
                self.neighbors.append(grid[prerow][col])

            if col < self.total_columns-1 and not grid[row][nextcol].is_barrier(): # Right
                self.neighbors.append(grid[row][nextcol])

            if col > 0 and not grid[row][precol].is_barrier():  # Left
                self.neighbors.append(grid[row][precol])

            if self.settings.diagonals and self.settings.consider_barrier == False:
                # Bottom-left
                if row < self.total_rows-1 and col > 0 and not grid[nextrow][precol].is_barrier():
                    self.neighbors.append(grid[nextrow][precol])

                # Bottom-right
                if row < self.total_rows-1 and col < self.total_columns-1 and not grid[nextrow][nextcol].is_barrier():
                    self.neighbors.append(grid[nextrow][nextcol])

                # Top-left
                if row > 0 and col > 0 and not grid[prerow][precol].is_barrier():
                    self.neighbors.append(grid[prerow][precol])

                # Top-right
                if row > 0 and col < self.total_columns-1 and not grid[prerow][nextcol].is_barrier():
                    self.neighbors.append(grid[prerow][nextcol])

            elif self.settings.diagonals and self.settings.consider_barrier:
                if row < self.total_rows-1 and col > 0 and not grid[nextrow][precol].is_barrier() and not grid[row][precol].is_barrier() \
                        and not grid[nextrow][col].is_barrier():  # Bottom-left and left and bottom are not barriers
                    self.neighbors.append(grid[nextrow][precol])

                if row < self.total_rows-1 and col < self.total_columns-1 and not grid[nextrow][nextcol].is_barrier() and not grid[row][nextcol].is_barrier() \
                        and not grid[nextrow][col].is_barrier():  # Bottom-right and right and bottom are not barriers
                    self.neighbors.append(grid[nextrow][nextcol])

                if row > 0 and col > 0 and not grid[prerow][precol].is_barrier() and not grid[row][precol].is_barrier()\
                        and not grid[prerow][col].is_barrier():  # Top-left and left and top are not barriers
                    self.neighbors.append(grid[prerow][precol])

                if row > 0 and col < self.total_columns-1 and not grid[prerow][nextcol].is_barrier() and not grid[row][nextcol].is_barrier()\
                        and not grid[prerow][col].is_barrier():  # Top-right and right and top are not barriers
                    self.neighbors.append(grid[prerow][nextcol])
