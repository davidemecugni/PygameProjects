import pygame
from time import sleep
from Settings import Settings
from Square import Square
from State import State
import sys


class GameOfLife():
    def __init__(self):
        self.settings = Settings()
        self.state = State()
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height))  # Sets the fullscreen
        pygame.display.set_caption(self.settings.caption)
        self.grid = self.make_grid(self.settings.rows,
                                   self.settings.columns, self.settings.width_of_squares, self.settings.height_of_squares)

    def run(self):
        x=0
        while self.state.run:
            self.check_events()
            if self.state.started:
                self.update_grid()
            self.draw(self.screen, self.grid, self.settings.rows,
                    self.settings.columns, self.settings.screen_width, self.settings.screen_height)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quits on X
                self.state.run = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.key_down_events(event)
            else:
                    # Left click
                    if pygame.mouse.get_pressed()[0] and not(self.state.started ):
                        self.get_clicked_square().make_alive()
                    # Right click
                    elif pygame.mouse.get_pressed()[2] and not (self.state.started ):
                        self.get_clicked_square().make_dead()
    def update_grid(self):
        for row in self.grid:
            for spot in row:
                spot.update_neighbors(self.grid)

        for row in self.grid:
            for spot in row:
                neighbors=len(spot.neighbors)
                if spot.is_alive() and not(neighbors==2 or neighbors==3):
                    spot.make_next_dead()
                elif spot.is_dead() and neighbors==3:
                    spot.make_next_alive()
                elif spot.is_alive():
                    spot.make_next_alive()
                elif spot.is_dead():
                    spot.make_next_dead()
                spot.update()

    def get_clicked_square(self):
        pos = pygame.mouse.get_pos()
        x,y = pos
        row = x // self.settings.width_of_squares
        col = y // self.settings.height_of_squares
        return self.grid[row][col]

    def key_down_events(self, event):
        """Does action related to pressing keys"""

        if event.key == pygame.K_ESCAPE:
            self.state.run = False
            sys.exit()

        if event.key == pygame.K_p:
            if self.settings.pacman:
                self.settings.pacman = False
            else:
                self.settings.pacman = True

        if event.key == pygame.K_c:
            self.state.started = False
            self.state.start = None
            self.state.end = None
            self.state.saved=False
            self.grid = self.make_grid(self.settings.rows,
                                       self.settings.columns, self.settings.width_of_squares, self.settings.height_of_squares)

        if event.key == pygame.K_s:
            if self.state.started:
                self.state.started = False
            else:
                self.state.started = True


        if event.key == pygame.K_SPACE and not self.state.started:
            self.state.started = True

                

                    
    def make_grid(self, tot_rows, tot_columns,  widthsquare, heightsquare):
        """Creates a matrix of squares"""
        grid = []
        for i in range(tot_rows):  # For every row and column adds a Square to grid
            grid.append([])
            for j in range(tot_columns):
                spot = Square(i, j, self.settings)
                grid[i].append(spot)
        return grid

    def draw_grid(self, window, rows, columns, width, height):
        """Draws the lines that divide squares"""
        for i in range(rows):
            pygame.draw.line(window, self.settings.line_color,
                             (0, i*self.settings.height_of_squares), (width, i*self.settings.height_of_squares),  self.settings.line_width)
            for j in range(columns):
                pygame.draw.line(window, self.settings.line_color,
                                 (i*self.settings.width_of_squares, 0), (i*self.settings.width_of_squares, height),  self.settings.line_width)

    def draw(self, window, grid, rows, columns, width, height):
        """Draws everything"""
        window.fill(self.settings.dead_color)
        for row in grid:
            for square in row:
                square.draw(window)
        self.draw_grid(window, rows, columns, width, height)
        pygame.display.update()


if __name__ == "__main__":
    game_of_life_istance = GameOfLife()
    game_of_life_istance.run()