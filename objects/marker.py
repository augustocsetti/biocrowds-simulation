from math import dist

import pygame
from config import *
from numpy import array

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
        self.rect = pygame.draw.circle(self.image, self.color, self.image.get_rect().center, 1)
        self.rect.center = position

        self.position = array(position, dtype=float)  
        self.owner = False

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.position, 1)

    def set_owner(self, agents):
        # search closest agent
        closest_agent = None
        closest_dist = 9999999999
        for agent in agents:
            distance = dist(self.rect.center, agent.position)
            if distance < closest_dist and distance < agent.sensor.radius:
                closest_agent = agent
                closest_dist = distance
        
        # check if agent is seeing marker
        if closest_agent:
            closest_agent.markers.append(self)
            self.owner = closest_agent
            self.set_color(closest_agent.color)
        else:
            self.owner = None
            self.set_color(self.color_base)      

    def set_color(self, color:tuple):
        self.color = color
        self.image.fill(color)
