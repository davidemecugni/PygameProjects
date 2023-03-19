import pygame
import math
from queue import PriorityQueue  # It's from std library anyway
from Settings import Settings
from Square import Square
from State import State
import sys


class Astarapp():
    def __init__(self):
        self.settings = Settings()
        self.state = State()
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height))  # Sets the fullscreen
        pygame.display.set_caption(self.settings.caption)
        self.grid = self.make_grid(self.settings.rows,
                                   self.settings.columns, self.settings.width_of_squares, self.settings.height_of_squares)

    def run(self):
        while self.state.run:
            self.check_events()
            # Draws depending on the settings
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
                    if pygame.mouse.get_pressed()[0] and not(self.state.a_star_started or self.state.saved):
                        spot = self.get_clicked_square()
                        if not self.state.start and spot != self.state.end:  # If !start and spot is not already end makes it
                            spot.make_start()
                            self.state.start = spot
                        elif not self.state.end and spot != self.state.start:  # If !end and spot is not already start makes it
                            spot.make_end()
                            self.state.end = spot
                        elif not spot.is_end() and not spot.is_start():  # If start and end makes barrier
                            spot.make_barrier()
                    # Right click
                    elif pygame.mouse.get_pressed()[2] and not (self.state.a_star_started or self.state.saved):
                        spot = self.get_clicked_square()
                        spot.make_bg()
                        if spot == self.state.start:
                            self.state.start = None
                        elif spot == self.state.end:
                            self.state.end = None

    def get_clicked_square(self):
        pos = pygame.mouse.get_pos()
        x,y = pos
        row = x // self.settings.width_of_squares
        col = y // self.settings.height_of_squares
        return self.grid[row][col]

    def key_down_events(self, event):
        """Does action related to pressing keys"""
        # ESC to close
        # P for pacman effect
        # 1 or 2 or 3 or 4 or 5 for different algorithms
        # C to clear
        # E to toggle showing the algorithm
        # UP and DOWN to fast or slow the algorithm
        # S to save
        # Space to start

        if event.key == pygame.K_ESCAPE:
            self.state.run = False
            sys.exit()
        if event.key == pygame.K_1:
            self.settings.heuristic = "dijkstra"
        if event.key == pygame.K_2:
            self.settings.heuristic = "taxicab"
        if event.key == pygame.K_3:
            self.settings.heuristic = "taxicabdiagonal"
        if event.key == pygame.K_4:
            self.settings.heuristic = "distance"
        if event.key == pygame.K_5:
            self.settings.heuristic = "maxdistance"

        if event.key == pygame.K_p:
            if self.settings.pacman:
                self.settings.pacman = False
            else:
                self.settings.pacman = True
            self.pacman_update(self.grid)

        if event.key == pygame.K_c:
            self.state.a_star_started = False
            self.state.start = None
            self.state.end = None
            self.state.saved=False
            self.grid = self.make_grid(self.settings.rows,
                                       self.settings.columns, self.settings.width_of_squares, self.settings.height_of_squares)

        if event.key == pygame.K_s:
            self.state.a_star_started = False
            self.state.saved=True
            self.clear_grid(self.grid)

        if event.key == pygame.K_e:
            if self.settings.showcalc:
                self.settings.showcalc = False
            else:
                self.settings.showcalc = True

        if event.key == pygame.K_UP:
            self.settings.interval_draw += 10
        if event.key == pygame.K_DOWN and self.settings.interval_draw > 5:
            self.settings.interval_draw -= 10
        # if space and A* didn't already started
        if event.key == pygame.K_SPACE and not self.state.a_star_started and self.state.start and self.state.end:
            self.state.a_star_started = True
            for row in self.grid:
                for spot in row:
                    spot.update_neighbors(self.grid)
            # Lambda is an anonymous function
            self.a_star(lambda: (self.draw(self.screen, self.grid, self.settings.rows,
                                      self.settings.columns, self.settings.screen_width, self.settings.screen_height)), lambda:(self.check_events()),lambda :(self.state.a_star_started == False),self.grid)

    def make_grid(self, tot_rows, tot_columns,  widthsquare, heightsquare):
        """Creates a matrix of squares"""
        grid = []
        for i in range(tot_rows):  # For every row and column adds a Square to grid
            grid.append([])
            for j in range(tot_columns):
                spot = Square(i, j, self.settings)
                grid[i].append(spot)
        return grid

    def pacman_update(self, grid):
        """Creates a matrix of squares"""
        i, j = 0, 0
        for row in grid:  # For every row and column adds a Square to grid
            for square in row:
                if square.is_barrier():
                    square = Square(i, j, self.settings)
                    square.make_barrier()
                elif square.is_start():
                    square = Square(i, j, self.settings)
                    square.make_start()
                elif square.is_end():
                    square = Square(i, j, self.settings)
                    square.make_end()
                j+=1
            i+=1

    def clear_grid(self, grid):
        """Clears the grid"""
        for row in grid:  # For every row and column adds a Square to grid
            for square in row:
                if not square.is_barrier():
                    square.make_bg()
        self.state.start.make_start()
        self.state.end.make_end()

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
        window.fill(self.settings.bg_color)
        for row in grid:
            for square in row:
                square.draw(window)
        self.draw_grid(window, rows, columns, width, height)
        pygame.display.update()


    def taxicabheuristic(self,p1, p2):  # sure shorter without diagonals
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1-x2)+abs(y1-y2)


    def taxicabheuristicdiagonal(self,p1, p2):  # excellent time with diagonals
        x1, y1 = p1
        x2, y2 = p2
        minimum = min([abs(x1-x2), abs(x1-x2)])
        # Subtract the shorter route throught a diagonal
        return ((abs(x1-x2)+abs(y1-y2))+(self.distanceheuristic(p1, p2))+(self.maxdistanceheuristic(p1, p2)))


    def distanceheuristic(self,p1, p2):  # Linear distance / Good time
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x1-x2)**2+(y1-y2)**2)


    def maxdistanceheuristic(self,p1, p2):  # Excess time / sure shortest for diagonals
        x1, y1 = p1
        x2, y2 = p2
        maximum = max([abs(x1-x2), abs(x1-x2)])
        return maximum


    def reconstruct_path(self,came_from, current, draw):
        # Until it finds the start aka the only one without a came_from
        # it draws the previous node
        # Speeds up the drawing
        partial_interval = self.settings.interval_draw_path
        while current in came_from:
            current = came_from[current]
            current.make_path()  # Draws it like path
            if self.settings.show_reversed_path == True:
                partial_interval -= 1
                if partial_interval == 0:
                    partial_interval = self.settings.interval_draw_path
                    draw()


    def a_star(self,draw, check_events,stopped, grid):
        partial_interval=self.settings.interval_draw
        start =self.state.start
        end =self.state.end
        pacman=self.settings.pacman
        # Speeds up the drawings
        count = 0
        open_set = PriorityQueue()  # Gets the lowest element

        # [0]=approx_score [1]=count [2]=current element
        open_set.put((0, count, start))

        came_from = {}

        # Associates for each and every square a inf amount of real_score
        real_score = {spot: float("inf")
                    for row in grid for spot in row}  # g-score
        real_score[start] = 0

        # Associates for each and every square a inf amount of approx_score
        approx_score = {spot: float("inf")
                        for row in grid for spot in row}  # f-score

        if self.settings.heuristic  == "dijkstra":# +0 because we're at start
            approx_score[start] = 0
        elif self.settings.heuristic  == "taxicab":
            approx_score[start] = self.taxicabheuristic(start.get_pos(), end.get_pos())  
        elif self.settings.heuristic  == "taxicabdiagonal":
            approx_score[start] = self.taxicabheuristicdiagonal(start.get_pos(), end.get_pos())  
        elif self.settings.heuristic  == "distance":
            approx_score[start] = self.distanceheuristic(start.get_pos(), end.get_pos())  
        elif self.settings.heuristic  == "maxdistance":
            approx_score[start] = self.maxdistanceheuristic(start.get_pos(), end.get_pos())  


        # Keeps the list of items that entered the priority queue
        open_set_hash = {start}

        while not open_set.empty():
            #heuristic=astar_istance.settings.heuristic
            # Quits if necessary
            check_events()
            #If the lambda returns true, stop everything
            if stopped():
                break
            # Gets the square out of the PQ that has the lowest approx score
            current = open_set.get()[2]
            # Removes it from the hash table
            open_set_hash.remove(current)
            if current == end:  # If the end is reached
                print(count)
                self.reconstruct_path(came_from, end, draw)
                end.make_end()  # Bc it is overwritten by the path
                start.make_start()  # Same
                return True
            for neighbor in current.neighbors:
                # Says that temp_real_score is 1 away from the old node
                temp_real_score = real_score[current]+1
                # Asks whether it found a better way to reach a neighbor than the one stored in
                # real_score and in that case updates the real_score, the approx_score
                # and stores the path in came_from
                if temp_real_score < real_score[neighbor]:
                    # Stores the path
                    came_from[neighbor] = current
                    # Updates real_score
                    real_score[neighbor] = temp_real_score

                    # Updates approx_score with heuristic given by lambda
                    heuristic=self.settings.heuristic
                    if heuristic == "dijkstra":
                        approx_score[neighbor] = temp_real_score

                    elif heuristic == "taxicab":
                        temp_approx_score = self.taxicabheuristic(
                            neighbor.get_pos(), end.get_pos())
                        if pacman:
                            y, x = end.get_pos()
                            temp_approx_score = min(temp_approx_score, self.taxicabheuristic(end.get_pos(), (0, y)), self.taxicabheuristic(
                                end.get_pos(), (x, 0)), self.taxicabheuristic(end.get_pos(), (x, astar_istance.settings.columns-1)), self.taxicabheuristic(end.get_pos(), (astar_istance.settings.rows-1, y)))
                        approx_score[neighbor] = temp_real_score + \
                            temp_approx_score

                    elif heuristic == "taxicabdiagonal":
                        temp_approx_score = self.taxicabheuristicdiagonal(
                            neighbor.get_pos(), end.get_pos())
                        if pacman:
                            y, x = end.get_pos()
                            temp_approx_score = min(temp_approx_score, self.taxicabheuristicdiagonal(end.get_pos(), (0, y)), self.taxicabheuristicdiagonal(
                                end.get_pos(), (x, 0)), self.taxicabheuristicdiagonal(end.get_pos(), (x, astar_istance.settings.columns-1)), self.taxicabheuristicdiagonal(end.get_pos(), (astar_istance.settings.rows-1, y)))
                        approx_score[neighbor] = temp_real_score + \
                            temp_approx_score

                    elif heuristic == "distance":
                        temp_approx_score = self.distanceheuristic(
                            neighbor.get_pos(), end.get_pos())
                        if pacman:
                            y, x = end.get_pos()
                            temp_approx_score = min(temp_approx_score, self.distanceheuristic(end.get_pos(), (0, y)), self.distanceheuristic(
                                end.get_pos(), (x, 0)), self.distanceheuristic(end.get_pos(), (x, astar_istance.settings.columns-1)), self.distanceheuristic(end.get_pos(), (astar_istance.settings.rows-1, y)))
                        approx_score[neighbor] = temp_real_score + \
                            temp_approx_score

                    elif heuristic == "maxdistance":
                        temp_approx_score = self.maxdistanceheuristic(
                            neighbor.get_pos(), end.get_pos())
                        if pacman:
                            y, x = end.get_pos()
                            temp_approx_score = min(temp_approx_score, self.maxdistanceheuristic(end.get_pos(), (0, y)), self.maxdistanceheuristic(
                                end.get_pos(), (x, 0)), self.maxdistanceheuristic(end.get_pos(), (x, astar_istance.settings.columns-1)), self.maxdistanceheuristic(end.get_pos(), (astar_istance.settings.rows-1, y)))
                        approx_score[neighbor] = temp_real_score + \
                            temp_approx_score

                    if neighbor not in open_set_hash:
                        count += 1  # Sets the ordinal for this open node
                        open_set.put((approx_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        # Colors the new found node
                        if neighbor.is_bg():
                            neighbor.make_open()
            if self.settings.showcalc == True:
                partial_interval -= 1
                if partial_interval == 0:
                    partial_interval = self.settings.interval_draw
                    draw()

            # Kills the old node
            if current != start:
                current.make_closed()
        return False  # If I didn't return True there isn't a path


if __name__ == "__main__":
    astar_istance = Astarapp()
    astar_istance.run()