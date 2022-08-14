import random
from math import ceil, dist

import pygame
from config import *
from numpy import array

from objects.grid import Grid
from objects.marker import Marker


class Field:
    def __init__(self, screen_size = array((SCREENWIDTH, SCREENHEIGHT)), grid_size=GRID) -> None:
        # splitting grids
        grid_x = ceil(screen_size[0] / grid_size)
        grid_y = ceil(screen_size[1] / grid_size)
        self.grid_len = array((grid_x, grid_y))
        self.grid_size = grid_size

        # creating grid sprites group
        self.grids_group = pygame.sprite.Group()
        for x in range (self.grid_len[0]):
            for y in range (self.grid_len[1]):
                self.grids_group.add(Grid((x, y), self.grid_size))

        # list to store created markers
        self.grids_markers = [[[] for i in range(self.grid_len[1])] for j in range(self.grid_len[0])]
        self.markers  = pygame.sprite.Group()

    def generate_markers(self, density = DENSITY, distance = DISTANCE):
        # list to iterate each new marker created
        markers_grid = []
        # running grids
        for x in range(0, self.grid_len[0]):
            for y in range(0, self.grid_len[1]):
                markers_grid.clear()
                # generating desire density in a grid
                m = 0
                while(m < density):
                    new_pos = (random.randint(x*self.grid_size, (x+1)*self.grid_size), random.randint(y*self.grid_size, (y+1)*self.grid_size))
                    space_available = True
                    for marker in markers_grid:
                        # evaluating the distance between the new marker and created markers
                        if dist(new_pos, marker.position) < distance:
                            space_available = False

                    if space_available:
                        new_marker = Marker(new_pos, color=MARKER_COLOR)
                        markers_grid.append(new_marker)
                        self.markers.add(new_marker)
                        self.grids_markers[x][y].append(new_marker)
                        m += 1
    
    def set_markers_owner_by_grid(self, agents:list, grid:tuple):
        x, y = grid
        for marker in self.grids_markers[x][y]:
            marker.set_owner(agents)

    def draw(self, window, draw_grid, draw_mark):
        if draw_grid:
            for grid in self.grids_group:
                grid.draw(window)
        if draw_mark:
            for marker in self.markers:
                marker.draw(window)        