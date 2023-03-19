"""Stores the settings for Astar"""
from pygame import Color, image


class Settings:
    """Stores all the settings from AI"""
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 1000
        self.columns = 100
        self.rows = self.columns
        self.width_of_squares = self.screen_width//self.columns
        self.height_of_squares = self.screen_height//self.rows
        self.caption = "A* algorithm"

        # Optimization

        self.diagonals = True
        # Defines if a diagonal barrier is legit in diagonal space
        self.consider_barrier = True
        #dijkstra = not informed, taxicab=perfect fot !diagonals,taxicabdiagonal=efficient,distance=not so useful,maxdistance = perfect
        #self.heuristic = "dijkstra"#Not informed
        self.heuristic = "taxicab"  # Top choice for taxicab space but slow
        #self.heuristic = "taxicabdiagonal" #Fastest choice
        #self.heuristic = "distance" #Test choice
        #self.heuristic="maxdistance" #Top choice for diagonal space except some walls but slow
        self.showcalc = False
        self.interval_draw = 1
        self.show_reversed_path = False
        self.interval_draw_path = 5
        self.pacman = False #Pacman universe
        # States
        self.start = None
        self.end = None
        self.run = True
        self.started = False
        # Color settings
        self.bg_color = Color("#ffffff")
        self.line_color = Color("#999999")
        self.line_width = 1
        self.barrier_color = Color("#000000")
        self.start_color = Color("#ffa500")
        self.end_color = Color("#b27300")
        self.path_color = Color("#0000ff")
        #self.open_color = Color("#fffffe")
        #self.closed_color = Color("#fffffd")
        self.open_color = Color("#1b7510")
        self.closed_color = Color("#6eeb34")
        