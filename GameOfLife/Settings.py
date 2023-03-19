"""Stores the settings for Astar"""
from pygame import Color, image


class Settings:
    """Stores all the settings from AI"""
    def __init__(self):
        self.screen_width = 800
        self.screen_height = self.screen_width
        self.columns = 80
        self.rows = self.columns
        self.width_of_squares = self.screen_width//self.columns
        self.height_of_squares = self.width_of_squares
        self.caption = "Game of life"
        self.pacman = False #Pacman universe
        # States
        self.start = None
        self.end = None
        self.run = True
        self.started = False
        # Color settings
        self.dead_color = Color("#ffffff")
        self.line_color = Color("#999999")
        self.line_width = 1
        self.alive_color = Color("#000000")
        