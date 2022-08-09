from math import dist, ceil
import random
import pygame
import numpy as np
from numpy import array

from config import *


CONT = 0

class Marker(pygame.sprite.Sprite):
    def __init__(self, position, color=RED) -> None:
        pygame.sprite.Sprite.__init__(self)    
        global CONT

        self.id = CONT
        CONT += 1

        self.color_base = color
        self.color = self.color_base
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        self.rect = pygame.draw.circle(self.image, self.color, self.image.get_rect().center, 2)
        self.rect.center = position

        self.position = array(position, dtype=float)  
        self.owner = False

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.position, 1)


    def set_owner(self, agents):
        closest_agent = None
        closest_dist = 9999999999
        for agent in agents:
            distance = dist(self.rect.center, agent.position)
            if distance < closest_dist:
                closest_agent = agent
                closest_dist = distance
        
        if closest_dist < VISION:
            closest_agent.markers.append(self)
            self.owner = closest_agent
            self.set_color(closest_agent.color)
        else:
            self.owner = None
            self.set_color(self.color_base)      

    def set_color(self, color:tuple):
        # self.color = color
        # self.image.fill(color)
        pass


class Field:
    def __init__(self, screen_size = array((SCREENWIDTH, SCREENHEIGHT)), grid_size=GRID) -> None:
        # splitting grids
        grid_x = ceil(screen_size[0] / grid_size)
        grid_y = ceil(screen_size[1] / grid_size)
        self.grid_len = array((grid_x, grid_y))

        self.grid_size = grid_size
                        
        # list to store created markers
        self.current_grid = [[[] for i in range(self.grid_len[1])] for j in range(self.grid_len[0])]
        self.markers  = []

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
                        self.markers.append(new_marker)
                        self.insert_into_grid(new_marker, grid=(x, y))
                        m += 1

    def insert_into_grid(self, marker:Marker, grid:array):
        # define neighborhood grids
        neighborhood = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                neighbor = grid + array((x, y))
                # check if grids values are inside screen
                if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < self.grid_len[0] and neighbor[1] < self.grid_len[1]:
                    neighborhood.append(neighbor)
        # add marker to neighborhood
        for n in neighborhood:
            self.current_grid[n[0]][n[1]].append(marker)

        # print(f'==================== NEW MARKER {marker.id} ====================')
        # for i in range(len(self.current_grid)):
        #     for j in range(len(self.current_grid[i])):
        #         if self.current_grid[i][j]:
        #             ids = []
        #             for m in self.current_grid[i][j]:
        #                 ids.append(m.id)
        #             print(f'grid:({i}, {j}): {ids}')

        # if m.id == 10:
        #     exit()   
        return
    
    def set_markers_owner_by_grid(self, agents:list, grid:tuple):
        x, y = grid
        for marker in self.current_grid[x][y]:
            marker.set_owner(agents)