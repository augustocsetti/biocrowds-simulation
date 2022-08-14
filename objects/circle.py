import pygame
from config import *
from numpy import array


class Circle(pygame.sprite.Sprite):
    def __init__(self, position, radius, color=WHITE) -> None:
        super().__init__()

        self.color = color
        self.radius = radius
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        self.rect = pygame.draw.circle(self.image, self.color, self.image.get_rect().center, self.radius, 1)
        self.rect.center = position

        self.position = array(position, dtype=float)  

    def draw(self, window):
        window.blit(self.image, self.rect)
        # pygame.draw.rect(window, self.color, self.image.get_rect())
