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
            self.settings.heuristic = "maxdistance"//Chess