import random
from math import dist, floor

import numpy as np
import pygame
from numpy import array, dot, zeros
from numpy.linalg import norm

from config import *

CONT = 0

def normalizeto(vector, max):
    if norm(vector) > 0:
        return (vector/norm(vector)) * max
    else:
        return zeros(2)    

class VisionSensor(pygame.sprite.Sprite):
    def __init__(self, position, orientation, ratio = VISION) -> None:
        pygame.sprite.Sprite.__init__(self)    

        self.radius = ratio
        self.image = pygame.Surface((ratio*2, ratio*2), pygame.SRCALPHA)
        self.rect = pygame.draw.circle(self.image, GREEN, self.image.get_rect().center, self.radius, 1)
        self.rect.center = position

    def update(self, position):
        self.rect.center = position

    def draw(self, window, color):
        # window.blit(self.image, self.rect)
        pygame.draw.circle(window, color, self.rect.center, self.radius, 1)  

    def check_visible_grids(self, grids_group:pygame.sprite.Group):
        return(pygame.sprite.spritecollide(self, grids_group, False))

class Agent(pygame.sprite.Sprite):
    def __init__(self, position, goal, color=None) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.on = True

        # agent id
        global CONT
        self.id = CONT
        CONT += 1
        
        if color:
            self.color = color
        else:
            self.color = (random.random() * 255*(2/3), random.random() * 255*(2/3), random.random() * 255*(2/3))

        self.size = 15
        self.position = array(position, dtype=float)       
        self.orientation = array((random.random(), random.random()))
        self.grid = (floor(position[0]/GRID), floor(position[1]/GRID))
        self.goal = goal

        # vision sensor
        self.sensor = VisionSensor(position, self.orientation)
        # list of closer markers
        self.markers = list()

    def hit_edges(self): # AQUI CONTINUAR
        # ref = GRID/4
        # if ( self.position[0] < -ref or
        #      self.position[1] < -ref or
        #      self.position[0] > SCREENWIDTH + ref or
        #      self.position[1] > SCREENHEIGHT + ref ):
        #     return True
        # else:
        #     return False
        return False

    def get_goal(self): # AQUI CONTINUAR
        # if (abs(self.position[0] - self.goal[0]) < GRID/4 and
        #     abs(self.position[1] - self.goal[1]) < GRID/4):
        #     return True
        # else:
        #     return False
        return False

    def update(self, window):
        '''
        function that handles an agents behavior
        '''
        # list to store the ponderation between goal and markers -> f(g, d)
        f_list = []
        for marker in self.markers:
            distance = dist(self.goal, marker.position)
            if distance:
                u = self.goal - self.position
                v = marker.position - self.position
                cos = dot(u,v) / 1 + (norm(u) * norm(v)) # -> cosine of the angle
                f = (1 + cos) / (1 + distance)
                # f = (1/(1 + distance)) * (1 + ((dot(u,v))/(norm(u)*norm(v))))
                f_list.append(f)
            else:
                f_list.append(0)

        # calculating the movement vector -> sum(w*d)
        f_sum = sum(f_list)
        m = zeros(2)
        for idx, f in enumerate(f_list):
            w = f / f_sum
            m += w * (self.markers[idx].position - self.position)

        # if the movement is not null calculate the instantaneous movement
        v = zeros(2)
        if norm(m) > 0.1: # AQUI
            s = min(norm(m), (S/FPS))
            v = s * (m / norm(m))
            self.position += v
            self.sensor.update(self.position)

        # set the new orientation
        if np.any(v):
            self.orientation = v

        # # log draws
        # pygame.draw.line(window, GREEN, self.position, self.position+m)
        # # for marker in self.markers:
        # #     pygame.draw.line(window, (55, 55, 55), self.position, marker.position)
        # # pygame.draw.circle(window, self.color, self.goal, 50)   

        # clean markers
        self.markers.clear()

        # update current grid
        current_grid = (floor(self.position[0]/GRID), floor(self.position[1]/GRID))
        if self.grid != current_grid:
            self.grid = current_grid

        # check if gegts the goal
        if self.get_goal():
            self.on = False        

    def draw(self, window: pygame.Surface):
        '''
        function that draws the agent
        '''
        # tip = normalizeto(self.orientation, self.size)
        # tiplineEnd = (self.position[0] + tip[0],
        #         self.position[1] + tip[1])

        # angle = math.atan2(self.orientation[0], self.orientation[1]) + (math.pi*0.85)
        # angle2 = math.atan2(self.orientation[0], self.orientation[1]) - (math.pi*0.85)
        # angleLineR = (self.position[0] + math.sin(angle) * self.size,
        #             self.position[1] + math.cos(angle) * self.size)
        # angleLineL = (self.position[0] + math.sin(angle2) * self.size,
        #             self.position[1] + math.cos(angle2) * self.size) 

        # pygame.draw.line(window, self.color, angleLineR, tiplineEnd,
        #                 max(1, int((self.size * self.size) / 100)))
        # pygame.draw.line(window, self.color, angleLineL, tiplineEnd,
        #                 max(1, int((self.size * self.size) / 100)))
        # pygame.draw.line(window, self.color, self.position, angleLineR,
        #                 max(1, int((self.size * self.size) / 100)))
        # pygame.draw.line(window, self.color, self.position, angleLineL,
        #                 max(1, int((self.size * self.size) / 100)))        

        # self draw
        pygame.draw.circle(window, self.color, self.position, 3)  

        # draw sensor
        # self.sensor.draw(window, self.color)    
